import React from 'react';

const SimilarTickets = ({ similarTickets }) => {
  return (
    <div className="card">
      <h3 className="card-title">Similar Tickets</h3>
      
      {similarTickets.length ? (
        <div className="space-y-4">
          {similarTickets.map((ticket, idx) => (
            <div key={idx} className="similar-ticket-item">
              <div className="similar-ticket-header">
                <div className="flex items-center">
                  <span className="ticket-counter">
                    {idx + 1}
                  </span>
                  <span style={{ fontSize: '0.875rem', color: 'var(--gray-500)' }}>
                    ID: {ticket.ticket_id}
                  </span>
                </div>
                <span className="badge badge-info">
                  {ticket.similarity_score.toFixed(2)}% Match
                </span>
              </div>
              
              <div style={{ marginLeft: '2.5rem' }} className="space-y-2">
                <div>
                  <span style={{ fontSize: '0.75rem', fontWeight: '500', color: 'var(--gray-500)' }}>Issue:</span>
                  <p style={{ fontSize: '0.875rem', color: 'var(--gray-800)' }}>{ticket.issue_description}</p>
                </div>
                
                <div>
                  <span style={{ fontSize: '0.75rem', fontWeight: '500', color: 'var(--gray-500)' }}>Category:</span>
                  <span className="badge badge-info" style={{ marginLeft: '0.25rem' }}>
                    {ticket.category}
                  </span>
                </div>
                
                <div>
                  <span style={{ fontSize: '0.75rem', fontWeight: '500', color: 'var(--gray-500)' }}>Resolution:</span>
                  <p style={{ fontSize: '0.875rem', color: 'var(--gray-800)', backgroundColor: 'white', padding: '0.5rem', borderRadius: 'var(--border-radius)', border: '1px solid var(--gray-200)', marginTop: '0.25rem' }}>
                    {ticket.resolution}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-similar-tickets">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" style={{ margin: '0 auto 12px', display: 'block', color: 'var(--gray-400)' }}>
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M9 10h.01"></path>
            <path d="M15 10h.01"></path>
            <path d="M9.5 15a3.5 3.5 0 0 0 5 0"></path>
          </svg>
          <p>No similar tickets found.</p>
        </div>
      )}
    </div>
  );
};

export default SimilarTickets;