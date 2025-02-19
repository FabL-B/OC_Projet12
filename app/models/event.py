from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from config.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    support_contact_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(1000), nullable=True)

    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="events")

    def __repr__(self):
        return repr({
            "id": self.id,
            "contract_id": self.contract_id,
            "support_contact_id": self.support_contact_id
        })
