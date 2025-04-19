import React, { useState } from 'react';
import axios from 'axios';

const TicketForm = ({ setTicket, setSimilarTickets, setSubmissionTime }) => {
  const [issue, setIssue] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!issue) return;

    setIsSubmitting(true);
    try {
      const response = await axios.post('http://localhost:8000/submit_ticket', {
        issue_description: issue
      });

      const ticketData = response.data;
      setTicket(ticketData);
      setSubmissionTime(new Date());

      const similarResponse = await axios.get(`http://localhost:8000/similar_tickets/${ticketData.ticket_id}`);
      setSimilarTickets(similarResponse.data);
    } catch (error) {
      console.error("Error submitting ticket:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2 className="card-title">Submit a New Support Ticket</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-group">
          <label className="form-label">
            Describe your issue:
          </label>
          <textarea
            className="form-control"
            rows="4"
            placeholder="Please provide details about your issue..."
            value={issue}
            onChange={(e) => setIssue(e.target.value)}
          />
        </div>
        <div>
          <button
            type="submit"
            disabled={isSubmitting || !issue.trim()}
            className={`btn btn-primary ${(isSubmitting || !issue.trim()) ? 'disabled' : ''}`}
          >
            {isSubmitting ? (
              <>
                <span className="spinner"></span>
                Processing...
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '8px' }}>
                  <path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                </svg>
                Submit Ticket
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TicketForm;