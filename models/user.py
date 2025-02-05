from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum("Sales", "Management", "Support", name="user_roles"),
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.now)

    customers = relationship("Customer", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")

    def __repr__(self):
        return repr({
            "id": self.id,
            "name": self.name,
            "role": self.role
        })
