
import { useState } from "react";
import "./App.css";

function App() {
  const [ticketId, setTicketId] = useState("");
  const [message, setMessage] = useState("");
  const [ticket, setTicket] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const API = "http://127.0.0.1:8000";

  async function submitTicket(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setTicket(null);

    try {
      const response = await fetch(`${API}/tickets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticket_id: ticketId,
          message: message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to create ticket");
      }

      setTicket(data);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "API connect nahi hui. Backend server check karo."
          : typeof err.message === "string"
            ? err.message
            : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  async function approveTicket() {
    if (!ticket) return;

    setError("");

    try {
      const response = await fetch(
        `${API}/tickets/${encodeURIComponent(ticket.ticket_id)}/approve`,
        { method: "POST" }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Approval failed");
      }

      setTicket((previous) => ({
        ...previous,
        approval_status: "approved",
        status: data.status || "ready",
      }));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">A</div>
          <div>
            <h2>AzureAssist</h2>
            <span>SUPPORT AUTOMATION</span>
          </div>
        </div>

        <p className="nav-label">WORKSPACE</p>
        <div className="nav-item active">▦ &nbsp; Ticket Dashboard</div>
        <div className="nav-item">◷ &nbsp; Review Queue</div>
        <div className="nav-item">⚙ &nbsp; Settings</div>

        <div className="sidebar-bottom">
          <div className="status-dot" />
          <span>Support system</span>
          <strong>Local</strong>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace / Dashboard</span>
            <h1>Support Ticket Dashboard</h1>
            <p>Classify tickets, generate responses, and review before approval.</p>
          </div>
          <div className="avatar">SA</div>
        </header>

        <section className="stats">
          <div className="stat-card">
            <span>Total submitted</span>
            <strong>{ticket ? "1" : "0"}</strong>
            <small>Tickets in this session</small>
          </div>
          <div className="stat-card">
            <span>Current category</span>
            <strong>{ticket ? ticket.category : "—"}</strong>
            <small>Automatically classified</small>
          </div>
          <div className="stat-card">
            <span>Approval status</span>
            <strong className="stat-status">
              {ticket ? ticket.approval_status || "pending" : "Pending"}
            </strong>
            <small>Human approval required</small>
          </div>
        </section>

        <section className="workspace">
          <div className="panel">
            <div className="panel-heading">
              <div>
                <h2>Create support ticket</h2>
                <p>Enter the ticket details to start AI-assisted processing.</p>
              </div>
              <span className="step-tag">STEP 01</span>
            </div>

            <form onSubmit={submitTicket}>
              <label htmlFor="ticketId">Ticket ID</label>
              <input
                id="ticketId"
                value={ticketId}
                onChange={(e) => setTicketId(e.target.value)}
                placeholder="e.g. TKT-1001"
                maxLength={30}
                required
              />

              <label htmlFor="message">Customer message</label>
              <textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Describe the customer's issue..."
                minLength={5}
                maxLength={2000}
                rows={6}
                required
              />

              <div className="form-footer">
                <span>{message.length}/2000 characters</span>
                <button type="submit" disabled={loading}>
                  {loading ? "Processing..." : "Process ticket →"}
                </button>
              </div>
            </form>

            {error && <div className="error-box">{error}</div>}
          </div>

          <div className="panel results-panel">
            <div className="panel-heading">
              <div>
                <h2>Ticket analysis</h2>
                <p>Classification and suggested response</p>
              </div>
              <span className="step-tag">STEP 02</span>
            </div>

            {!ticket ? (
              <div className="empty-state">
                <div className="empty-icon">✳</div>
                <h3>Ready to analyze</h3>
                <p>Submit a ticket to see its category, priority, assigned team, summary, and draft response here.</p>
              </div>
            ) : (
              <div className="ticket-result">
                <div className="result-top">
                  <span className="ticket-number">{ticket.ticket_id}</span>
                  <span className={`pill ${ticket.needs_review ? "review" : "success"}`}>
                    {ticket.needs_review ? "Needs review" : "Classified"}
                  </span>
                </div>

                <div className="result-grid">
                  <div className="result-field">
                    <span>CATEGORY</span>
                    <strong>{ticket.category}</strong>
                  </div>
                  <div className="result-field">
                    <span>PRIORITY</span>
                    <strong>{ticket.priority}</strong>
                  </div>
                  <div className="result-field full">
                    <span>ASSIGNED TEAM</span>
                    <strong>{ticket.assigned_team}</strong>
                  </div>
                  <div className="result-field full">
                    <span>SUMMARY</span>
                    <p>{ticket.summary || ticket.message}</p>
                  </div>
                </div>

                <div className="draft-box">
                  <h3>Suggested response</h3>
                  <p>{ticket.draft_response}</p>
                  <span>Draft only · No email will be sent</span>
                </div>

                <div className="approval-row">
                  <div>
                    <strong>Human approval</strong>
                    <p>
                      Status: {ticket.status || "pending"}
                    </p>
                  </div>
                  <button
                    className="approve-button"
                    onClick={approveTicket}
                    disabled={ticket.approval_status === "approved"}
                  >
                    {ticket.approval_status === "approved"
                      ? "✓ Approved"
                      : "Approve draft"}
                  </button>
                </div>
              </div>
            )}
          </div>
        </section>

        <footer>AzureAssist · Support Ticket Automation</footer>
      </main>
    </div>
  );
}

export default App;
