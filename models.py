
from sqlalchemy import Column, String, Text, Boolean
from database import Base

class TicketRecord(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String(30), primary_key=True)
    message = Column(Text, nullable=False)
    summary = Column(Text, nullable=False, default="")
    category = Column(String(30), nullable=False)
    priority = Column(String(20), nullable=False)
    assigned_team = Column(String(50), nullable=False)
    draft_response = Column(Text, nullable=False)
    approval_status = Column(
        String(20), default="pending", nullable=False
    )
    status = Column(String(20), default="pending", nullable=False)

    needs_review = Column(Boolean, default=False, nullable=False)