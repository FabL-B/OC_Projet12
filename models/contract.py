from sqlalchemy import Column, Integer, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    status = Column(
        Enum("unsigned", "signed", name="contract_status"),
        nullable=False,
        default="unsigned"
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    customer = relationship("Customer", back_populates="contracts")

    @property
    def sales_contact_id(self):
        return self.customer.sales_contact_id

    def __repr__(self):
        return repr({
            "id": self.id,
            "customer_id": self.customer_id,
            "status": self.status,
        })
