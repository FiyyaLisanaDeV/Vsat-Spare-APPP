import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base


class ServicePointType(str, enum.Enum):
    service_representative = "service_representative"
    subcon = "subcon"
    pic_lokasi = "pic_lokasi"


class ServicePoint(Base):
    __tablename__ = "service_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ServicePointType), nullable=False)
    city = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    pic_name = Column(String(255), nullable=False)
    pic_phone = Column(String(20), nullable=False)
    pic_email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    users = relationship("User", back_populates="service_point")
    stocks = relationship("Stock", back_populates="service_point")
