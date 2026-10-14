# Azure Support Ticket Automation

## Overview
Azure Support Ticket Automation is a web-based application that helps classify support tickets, assign them to the appropriate support team, suggest priority, generate a short summary, and draft a response for human review.

## Features
- Automatically categorizes tickets as Billing, Technical, Access, or General.
- Assigns ticket priority: High, Medium, or Low.
- Routes tickets to the appropriate support team.
- Generates a short summary and draft response.
- Flags General tickets for human review.
- Supports ticket approval before marking a draft as ready.
- Rejects duplicate ticket IDs and invalid inputs.
- Stores ticket information in an SQLite database.
- Provides a React dashboard and FastAPI backend.

## Technology Stack
- Frontend: React, Vite, CSS
- Backend: Python, FastAPI
- Database: SQLite, SQLAlchemy
- Testing: Pytest
- Containerization: Docker
- CI: GitHub Actions

## Run Locally

### 1. Create and activate a virtual environment
```bash
python -m venv venv
```

Windows:
```cmd
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the backend
```bash
uvicorn main:app --reload
```

Open http://localhost:8000/docs to explore the API.

### 4. Start the frontend
Open another terminal:
```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually http://localhost:5173.

## Run Tests
```bash
python -m pytest -v
```

## Evaluate Classification
```bash
python evaluate.py
```

The current held-out evaluation reports **80% category accuracy (8 correct predictions out of 10 test examples)**. This is a small test set, so the result should not be interpreted as a guarantee of real-world performance.

## Run with Docker
Build the image:
```bash
docker build -t azure-ticket-automation .
```

Run the API:
```bash
docker run --name azure-ticket-test -p 8000:8000 azure-ticket-automation
```

Open http://localhost:8000/docs.

## API Endpoints
- `GET /` — Check API status.
- `POST /tickets` — Create and classify a support ticket.
- `GET /tickets/{ticket_id}` — Retrieve ticket details.
- `POST /tickets/{ticket_id}/approve` — Approve a draft and mark it ready.

## Human Review
The application creates draft responses only. Approval is required before a ticket is marked ready. It does not send real emails or customer messages.

## Dataset and Evaluation
The sample dataset is stored in `data/tickets.json` and contains 30 fictional labeled tickets. The evaluation script uses 20 reference examples and 10 held-out examples.

## Future Improvements
- Replace keyword-based classification with a trained or semantic classifier.
- Improve category and priority accuracy using a larger, balanced dataset.
- Add authentication and role-based access control.
- Deploy the backend to Microsoft Azure.
