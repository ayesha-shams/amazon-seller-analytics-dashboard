"""
Generates realistic synthetic seller data so the dashboard has something to
show without needing live Amazon SP-API access (which requires seller
approval and is slow to get sandboxed access to).

Be upfront about this in your README -- it's completely normal for a
portfolio project and shows good judgment about scoping, not a shortcut
you need to hide.

Run with: python -m scripts.generate_data   (from the backend/ directory)
"""
import random
from datetime import date, timedelta

from faker import Faker
from app.database import Base, engine, SessionLocal
from app.models.models import Product, Order, InventorySnapshot, AdSpend

fake = Faker()
random.seed(42)  # reproducible data

CATEGORIES = ["Kitchen", "Home & Garden", "Electronics Accessories", "Pet Supplies", "Sports & Outdoors"]
NUM_PRODUCTS = 12
DAYS_OF_HISTORY = 90


def generate():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Wipe existing data so this script is safely re-runnable
    db.query(AdSpend).delete()
    db.query(InventorySnapshot).delete()
    db.query(Order).delete()
    db.query(Product).delete()
    db.commit()

    products = []
    for _ in range(NUM_PRODUCTS):
        cost = round(random.uniform(3, 40), 2)
        product = Product(
            asin="B0" + fake.bothify(text="???######").upper(),
            name=fake.catch_phrase() + " " + random.choice(["Pro", "Deluxe", "Set", "Kit", ""]),
            category=random.choice(CATEGORIES),
            cost_price=cost,
            sale_price=round(cost * random.uniform(1.8, 3.2), 2),
            lead_time_days=random.choice([7, 14, 21, 30]),
        )
        db.add(product)
        products.append(product)
    db.commit()

    start_date = date.today() - timedelta(days=DAYS_OF_HISTORY)

    for product in products:
        # Give each product a "popularity" baseline so some sell much better than others
        base_daily_units = random.randint(1, 25)
        stock = random.randint(200, 1000)

        for day_offset in range(DAYS_OF_HISTORY):
            current_date = start_date + timedelta(days=day_offset)

            # --- Orders: add some day-to-day noise and a slight upward trend ---
            trend_factor = 1 + (day_offset / DAYS_OF_HISTORY) * 0.3
            units_today = max(0, int(random.gauss(base_daily_units * trend_factor, base_daily_units * 0.3)))
            revenue_today = round(units_today * product.sale_price, 2)

            if units_today > 0:
                db.add(Order(
                    product_id=product.id,
                    order_date=current_date,
                    units_sold=units_today,
                    revenue=revenue_today,
                ))

            # --- Inventory: decreases with sales, occasionally restocks ---
            stock -= units_today
            if stock < 50 and random.random() < 0.3:
                stock += random.randint(300, 600)  # simulate a restock event
            stock = max(stock, 0)

            db.add(InventorySnapshot(
                product_id=product.id,
                snapshot_date=current_date,
                units_in_stock=stock,
            ))

            # --- Ad spend: only on ~70% of days, roughly tied to unit velocity ---
            if random.random() < 0.7:
                spend_today = round(random.uniform(5, 60), 2)
                clicks_today = max(1, int(spend_today / random.uniform(0.4, 1.2)))
                impressions_today = clicks_today * random.randint(20, 80)
                attributed_sales_today = round(spend_today * random.uniform(1.5, 6.0), 2)

                db.add(AdSpend(
                    product_id=product.id,
                    spend_date=current_date,
                    spend=spend_today,
                    clicks=clicks_today,
                    impressions=impressions_today,
                    attributed_sales=attributed_sales_today,
                ))

    db.commit()
    db.close()
    print(f"Generated {NUM_PRODUCTS} products with {DAYS_OF_HISTORY} days of order, inventory, and ad spend history.")


if __name__ == "__main__":
    generate()
