"""
Core data model for the dashboard.

Kept intentionally normalized: products are the anchor entity, and orders,
inventory snapshots, and ad spend all reference back to a product. This
mirrors how a real seller data model would look and is a good thing to be
able to explain in an interview.
"""
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String, unique=True, index=True)  # Amazon Standard ID Number
    name = Column(String, nullable=False)
    category = Column(String)
    cost_price = Column(Float)          # what it costs the seller
    sale_price = Column(Float)          # current listing price
    lead_time_days = Column(Integer, default=14)  # restock lead time, used for reorder calc

    orders = relationship("Order", back_populates="product")
    inventory_snapshots = relationship("InventorySnapshot", back_populates="product")
    ad_spend_entries = relationship("AdSpend", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(Date, index=True)
    units_sold = Column(Integer)
    revenue = Column(Float)

    product = relationship("Product", back_populates="orders")


class InventorySnapshot(Base):
    __tablename__ = "inventory_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    snapshot_date = Column(Date, index=True)
    units_in_stock = Column(Integer)

    product = relationship("Product", back_populates="inventory_snapshots")


class AdSpend(Base):
    __tablename__ = "ad_spend"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    spend_date = Column(Date, index=True)
    spend = Column(Float)
    clicks = Column(Integer)
    impressions = Column(Integer)
    attributed_sales = Column(Float)  # revenue attributed to this ad spend (for ROAS)

    product = relationship("Product", back_populates="ad_spend_entries")
