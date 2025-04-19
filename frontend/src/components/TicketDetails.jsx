import React from 'react';

const TicketDetails = ({ ticket, finalResponse }) => {
  return (
    <div className="card mb-6">
      <h3 className="card-title">Ticket Details</h3>
      
      <div className="space-y-2">
        <div className="ticket-field">
          <span className="ticket-label">ID:</span>
          <span className="ticket-value">{ticket.ticket_id}</span>
        </div>
        
        <div className="ticket-field">
          <span className="ticket-label">Issue:</span>
          <span className="ticket-value">{ticket.issue_description}</span>
        </div>
        
        <div className="ticket-field">
          <span className="ticket-label">Predicted Category:</span>
          <span className="badge badge-info">{ticket.category}</span>
        </div>
        
        <div className="ticket-field">
          <span className="ticket-label">Confirmed Category:</span>
          {ticket.confirmed_category ? (
            <span className="badge badge-success">{ticket.confirmed_category}</span>
          ) : (
            <span className="badge badge-warning">Not yet confirmed</span>
          )}
        </div>
        
        <div className="ticket-field">
          <span className="ticket-label">Status:</span>
          {finalResponse ? (
            <span className="badge badge-success">Resolved</span>
          ) : (
            <span className="badge badge-warning">Pending</span>
          )}
        </div>
        
        <div className="ticket-field" style={{ marginTop: '16px' }}>
          <p className="ticket-label mb-2">Draft Response:</p>
          <div className="draft-response">
            {ticket.draft_response}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketDetails;