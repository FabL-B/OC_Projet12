from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(100), unique=True, nullable=False)
    sales_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    contracts = relationship("Contract", back_populates="customer")
    sales_contact = relationship("User", back_populates="customers")

    def __repr__(self):
        return repr({
            "id": self.id,
            "name": self.name,
            "company": self.company_name
        })
