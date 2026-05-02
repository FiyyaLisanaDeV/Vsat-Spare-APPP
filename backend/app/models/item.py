from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class ItemType(Base):
    __tablename__ = "item_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    categories = relationship("ItemCategory", back_populates="item_type")
    spare_items = relationship("SpareItem", back_populates="item_type")


class ItemCategory(Base):
    __tablename__ = "item_categories"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("item_types.id"), nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    item_type = relationship("ItemType", back_populates="categories")
    spare_items = relationship("SpareItem", back_populates="item_category")


class SpareItem(Base):
    __tablename__ = "spare_items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type_id = Column(Integer, ForeignKey("item_types.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("item_categories.id"), nullable=False)
    unit = Column(String(50), nullable=False)
    requires_serial = Column(Boolean, default=False, nullable=False)
    min_stock = Column(Integer, default=0, nullable=False)
    catatan = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    item_type = relationship("ItemType", back_populates="spare_items")
    item_category = relationship("ItemCategory", back_populates="spare_items")
    stocks = relationship("Stock", back_populates="spare_item")
