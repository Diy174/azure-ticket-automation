from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_create_ticket():
    response = client.post(
        "/tickets",
        json={
            "ticket_id": "TEST406",
            "message": "My payment failed and I need help"
        }
    )
    assert response.status_code == 200
    assert response.json()["category"] == "Billing"


def test_duplicate_ticket():
    ticket = {
        "ticket_id": "TEST102",
        "message": "I need help with my invoice"
    }

    client.post("/tickets", json=ticket)
    response = client.post("/tickets", json=ticket)

    assert response.status_code == 409


def test_invalid_ticket():
    response = client.post(
        "/tickets",
        json={"ticket_id": "", "message": "Hi"}
    )
    assert response.status_code == 422


def test_ticket_not_found():
    response = client.get("/tickets/UNKNOWN999")
    assert response.status_code == 404

def test_approve_ticket():
    ticket = {
        "ticket_id": "TEST103",
        "message": "I need a refund for my payment"
    }

    client.post("/tickets", json=ticket)

    response = client.post("/tickets/TEST103/approve")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_ambiguous_ticket_needs_review():
    response = client.post(
        "/tickets",
        json={
            "ticket_id": "TEST405",
            "message": "I have a question about my situation"
        }
    )

    assert response.status_code == 200
    assert response.json()["needs_review"] is True


