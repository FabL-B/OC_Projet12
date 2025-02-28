from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False
    )
    amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="unsigned")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    customer = relationship("Customer", back_populates="contracts")
    events = relationship(
        "Event",
        back_populates="contract",
        cascade="all, delete"
    )

    ALLOWED_STATUSES = {"unsigned", "signed"}

    def set_status(self, new_status):
        """Validates and sets the contract status."""
        if new_status not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {new_status}. Allowed statuses: {self.ALLOWED_STATUSES}")
        self.status = new_status

    @property
    def sales_contact_id(self):
        return self.customer.sales_contact_id

    def __repr__(self):
        return repr({
            "id": self.id,
            "customer_id": self.customer_id,
            "status": self.status,
        })
