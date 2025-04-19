// AgentActions.jsx
import React, { useState } from 'react';
import axios from 'axios';

const AgentActions = ({ ticket, setTicket, setFinalResponse, setResolutionTime }) => {
  const [category, setCategory] = useState(ticket.category);
  const [draft, setDraft] = useState(ticket.draft_response);
  const [isSubmittingCategory, setIsSubmittingCategory] = useState(false);
  const [isSubmittingResponse, setIsSubmittingResponse] = useState(false);

  const approveCategory = async () => {
    if (!category) return;
    
    setIsSubmittingCategory(true);
    try {
      await axios.put(`http://localhost:8000/approve_category/${ticket.ticket_id}`, {
        confirmed_category: category,
      });
      setTicket({ ...ticket, confirmed_category: category });
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmittingCategory(false);
    }
  };

  const approveResponse = async () => {
    if (!draft) return;
    
    setIsSubmittingResponse(true);
    try {
      await axios.put(`http://localhost:8000/approve_ticket/${ticket.ticket_id}`, {
        final_response: draft,
      });
      setFinalResponse(draft);
      setResolutionTime(new Date());
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmittingResponse(false);
    }
  };

  return (
    <div className="card">
      <h3 className="card-title">Agent Actions</h3>
      
      <div className="space-y-4">
        <div>
          <label className="form-label">
            Confirm Category
          </label>
          <div className="flex space-x-2">
            <input 
              type="text"
              className="form-control"
              style={{ flex: 1 }}
              value={category} 
              onChange={(e) => setCategory(e.target.value)} 
            />
            <button 
              onClick={approveCategory}
              disabled={isSubmittingCategory || !category.trim()}
              className={`btn btn-success ${(isSubmittingCategory || !category.trim()) ? 'disabled' : ''}`}
            >
              {isSubmittingCategory ? (
                <span className="spinner"></span>
              ) : "Approve"}
            </button>
          </div>
        </div>
        
        <div>
          <label className="form-label">
            Edit Draft Response
          </label>
          <textarea 
            className="form-control mb-4"
            rows="6"
            value={draft} 
            onChange={(e) => setDraft(e.target.value)} 
          />
          <button 
            onClick={approveResponse}
            disabled={isSubmittingResponse || !draft.trim()}
            className={`btn btn-primary w-full ${(isSubmittingResponse || !draft.trim()) ? 'disabled' : ''}`}
          >
            {isSubmittingResponse ? (
              <>
                <span className="spinner"></span>
                Processing...
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '8px' }}>
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                Approve & Submit Response
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentActions;