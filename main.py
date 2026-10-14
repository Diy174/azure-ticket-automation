from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import TicketRecord
from init_db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def classify_category(message: str) -> str:
    message = message.lower()

    if any(word in message for word in [
        "refund", "payment", "billing", "invoice", "charged"
    ]):
        return "Billing"
    elif any(word in message for word in [
        "error", "bug", "crash", "not working", "failed"
    ]):
        return "Technical"
    elif any(word in message for word in [
        "login", "password", "access", "locked"
    ]):
        return "Access"
    else:
        return "General"


class Ticket(BaseModel):
    ticket_id: str = Field(min_length=1, max_length=30)
    message: str = Field(min_length=5, max_length=2000)


@app.get("/")
def home():
    return {"message": "Azure Ticket Automation API is running!"}


@app.post("/tickets")
def create_ticket(ticket: Ticket):
    db: Session = SessionLocal()

    try:
        existing_ticket = db.get(TicketRecord, ticket.ticket_id)

        if existing_ticket:
            raise HTTPException(
                status_code=409,
                detail="Ticket ID already exists"
            )

        message = ticket.message.lower()
        category = classify_category(ticket.message)

        needs_review = category == "General"

        summary = ticket.message[:100]

        urgent_words = [
            "urgent", "immediately", "critical", "emergency", "outage"
        ]

        if any(word in message for word in urgent_words):
            priority = "High"
        elif any(word in message for word in [
            "soon", "delayed", "waiting"
        ]):
            priority = "Medium"
        else:
            priority = "Low"

        teams = {
            "Billing": "Billing Support",
            "Technical": "Technical Support",
            "Access": "Account Support",
            "General": "General Support"
        }
        assigned_team = teams[category]

        responses = {
            "Billing": (
                "Thank you for contacting us. Our Billing Support team "
                "will review your payment or refund issue."
            ),
            "Technical": (
                "Thank you for reporting this issue. Our Technical "
                "Support team will investigate it."
            ),
            "Access": (
                "Thank you for contacting us. Our Account Support team "
                "will help resolve your access issue."
            ),
            "General": (
                "Thank you for contacting support. Our team will review "
                "your request and get back to you."
            )
        }
        draft_response = responses[category]

        record = TicketRecord(
            ticket_id=ticket.ticket_id,
            message=ticket.message,
            summary=summary,
            category=category,
            priority=priority,
            assigned_team=assigned_team,
            draft_response=draft_response,
            approval_status="pending",
            status="pending",
            needs_review=needs_review,
        )

        db.add(record)
        db.commit()

        return {
            "ticket_id": record.ticket_id,
            "message": record.message,
            "summary": record.summary,
            "category": record.category,
            "priority": record.priority,
            "assigned_team": record.assigned_team,
            "draft_response": record.draft_response,
            "approval_status": record.approval_status,
            "needs_review": record.needs_review,
            "status": "Ticket received successfully"
        }

    finally:
        db.close()


@app.post("/tickets/{ticket_id}/approve")
def approve_ticket(ticket_id: str):
    db: Session = SessionLocal()

    try:
        record = db.get(TicketRecord, ticket_id)

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        record.approval_status = "approved"
        record.status = "ready"
        db.commit()

        return {
            "ticket_id": record.ticket_id,
            "approval_status": record.approval_status,
            "status": record.status
        }

    finally:
        db.close()


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    db: Session = SessionLocal()

    try:
        record = db.get(TicketRecord, ticket_id)

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        return {
            "ticket_id": record.ticket_id,
            "message": record.message,
            "summary": record.summary,
            "category": record.category,
            "priority": record.priority,
            "assigned_team": record.assigned_team,
            "draft_response": record.draft_response,
            "approval_status": record.approval_status,
            "needs_review": record.needs_review,
            "status": record.status
        }

    finally:
        db.close()
