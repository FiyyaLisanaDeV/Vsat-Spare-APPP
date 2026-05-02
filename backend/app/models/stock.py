from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    service_point_id = Column(
        Integer, ForeignKey("service_points.id"), nullable=False
    )
    spare_item_id = Column(
        Integer, ForeignKey("spare_items.id"), nullable=False
    )
    qty = Column(Integer, default=0, nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    __table_args__ = (
        UniqueConstraint("service_point_id", "spare_item_id", name="uq_stock_sp_item"),
    )

    service_point = relationship("ServicePoint", back_populates="stocks")
    spare_item = relationship("SpareItem", back_populates="stocks")
    updated_by_user = relationship("User", back_populates="stock_updates")
