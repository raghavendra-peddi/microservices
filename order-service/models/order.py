from database import Base
from sqlalchemy import Integer, Float, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    order_items: Mapped[list["OrderInventoryItem"]] = relationship("OrderInventoryItem", back_populates="order")