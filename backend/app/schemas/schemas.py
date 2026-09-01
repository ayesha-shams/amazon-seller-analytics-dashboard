from datetime import date
from pydantic import BaseModel


class ProductOut(BaseModel):
    id: int
    asin: str
    name: str
    category: str
    sale_price: float

    class Config:
        from_attributes = True


class RevenuePoint(BaseModel):
    date: date
    revenue: float
    units_sold: int


class InventoryAlert(BaseModel):
    product_id: int
    product_name: str
    units_in_stock: int
    daily_velocity: float
    days_of_stock_left: float
    reorder_point: int
    needs_reorder: bool


class AdPerformance(BaseModel):
    product_id: int
    product_name: str
    total_spend: float
    total_attributed_sales: float
    roas: float  # return on ad spend = attributed_sales / spend


class KpiSummary(BaseModel):
    total_revenue_30d: float
    total_units_30d: int
    total_ad_spend_30d: float
    average_roas_30d: float
    products_needing_reorder: int
