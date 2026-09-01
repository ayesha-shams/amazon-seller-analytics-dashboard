"""
This is the heart of the project: real aggregation logic over the raw
order/inventory/ad-spend tables, rather than just dumping rows back to the
frontend. This is what shows "engineering judgment" rather than CRUD.
"""
from datetime import date, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.models import Product, Order, InventorySnapshot, AdSpend
from app.schemas.schemas import RevenuePoint, InventoryAlert, AdPerformance, KpiSummary

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/revenue-trend", response_model=list[RevenuePoint])
def revenue_trend(days: int = 30, db: Session = Depends(get_db)):
    """Daily revenue and units sold across all products for the last N days."""
    cutoff = date.today() - timedelta(days=days)

    rows = (
        db.query(
            Order.order_date,
            func.sum(Order.revenue).label("revenue"),
            func.sum(Order.units_sold).label("units_sold"),
        )
        .filter(Order.order_date >= cutoff)
        .group_by(Order.order_date)
        .order_by(Order.order_date)
        .all()
    )

    return [RevenuePoint(date=r.order_date, revenue=round(r.revenue, 2), units_sold=r.units_sold) for r in rows]


@router.get("/inventory-alerts", response_model=list[InventoryAlert])
def inventory_alerts(velocity_window_days: int = 14, db: Session = Depends(get_db)):
    """
    For each product, estimate sales velocity (avg units/day) over a recent
    window, compare it to current stock and lead time, and flag anything
    that will run out before a restock could arrive.

    reorder_point = daily_velocity * lead_time_days * 1.2 (buffer)
    This is a simplified version of a real reorder-point formula sellers use.
    """
    cutoff = date.today() - timedelta(days=velocity_window_days)
    products = db.query(Product).all()
    alerts = []

    for product in products:
        recent_units = (
            db.query(func.sum(Order.units_sold))
            .filter(Order.product_id == product.id, Order.order_date >= cutoff)
            .scalar() or 0
        )
        daily_velocity = round(recent_units / velocity_window_days, 2)

        latest_snapshot = (
            db.query(InventorySnapshot)
            .filter(InventorySnapshot.product_id == product.id)
            .order_by(InventorySnapshot.snapshot_date.desc())
            .first()
        )
        units_in_stock = latest_snapshot.units_in_stock if latest_snapshot else 0

        days_of_stock_left = round(units_in_stock / daily_velocity, 1) if daily_velocity > 0 else float("inf")
        reorder_point = int(daily_velocity * product.lead_time_days * 1.2)
        needs_reorder = units_in_stock <= reorder_point

        alerts.append(InventoryAlert(
            product_id=product.id,
            product_name=product.name,
            units_in_stock=units_in_stock,
            daily_velocity=daily_velocity,
            days_of_stock_left=days_of_stock_left if days_of_stock_left != float("inf") else -1,
            reorder_point=reorder_point,
            needs_reorder=needs_reorder,
        ))

    # Most urgent first
    alerts.sort(key=lambda a: a.days_of_stock_left if a.days_of_stock_left >= 0 else 9999)
    return alerts


@router.get("/ad-performance", response_model=list[AdPerformance])
def ad_performance(days: int = 30, db: Session = Depends(get_db)):
    """ROAS (return on ad spend) per product over the last N days."""
    cutoff = date.today() - timedelta(days=days)

    rows = (
        db.query(
            AdSpend.product_id,
            Product.name,
            func.sum(AdSpend.spend).label("total_spend"),
            func.sum(AdSpend.attributed_sales).label("total_attributed_sales"),
        )
        .join(Product, Product.id == AdSpend.product_id)
        .filter(AdSpend.spend_date >= cutoff)
        .group_by(AdSpend.product_id, Product.name)
        .all()
    )

    results = []
    for r in rows:
        roas = round(r.total_attributed_sales / r.total_spend, 2) if r.total_spend else 0
        results.append(AdPerformance(
            product_id=r.product_id,
            product_name=r.name,
            total_spend=round(r.total_spend, 2),
            total_attributed_sales=round(r.total_attributed_sales, 2),
            roas=roas,
        ))

    results.sort(key=lambda x: x.roas, reverse=True)
    return results


@router.get("/kpi-summary", response_model=KpiSummary)
def kpi_summary(db: Session = Depends(get_db)):
    """Top-line numbers for the dashboard header cards."""
    cutoff = date.today() - timedelta(days=30)

    revenue_units = (
        db.query(func.sum(Order.revenue), func.sum(Order.units_sold))
        .filter(Order.order_date >= cutoff)
        .first()
    )
    total_revenue = revenue_units[0] or 0
    total_units = revenue_units[1] or 0

    ad_totals = (
        db.query(func.sum(AdSpend.spend), func.sum(AdSpend.attributed_sales))
        .filter(AdSpend.spend_date >= cutoff)
        .first()
    )
    total_ad_spend = ad_totals[0] or 0
    total_attributed_sales = ad_totals[1] or 0
    avg_roas = round(total_attributed_sales / total_ad_spend, 2) if total_ad_spend else 0

    reorder_alerts = inventory_alerts(db=db)
    products_needing_reorder = sum(1 for a in reorder_alerts if a.needs_reorder)

    return KpiSummary(
        total_revenue_30d=round(total_revenue, 2),
        total_units_30d=total_units,
        total_ad_spend_30d=round(total_ad_spend, 2),
        average_roas_30d=avg_roas,
        products_needing_reorder=products_needing_reorder,
    )
