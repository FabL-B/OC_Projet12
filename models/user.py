from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from config.database import Base


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

    ph = PasswordHasher()

    def set_password(self, password: str):
        self.password_hash = self.ph.hash(password)

    def verify_password(self, password: str) -> bool:
        try:
            return self.ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

    def __repr__(self):
        return repr({
            "id": self.id,
            "name": self.name,
            "role": self.role
        })
