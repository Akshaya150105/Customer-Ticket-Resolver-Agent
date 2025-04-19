import React, { useState } from 'react';
import TicketForm from './components/TicketForm';
import TicketDetails from './components/TicketDetails';
import AgentActions from './components/AgentActions';
import SimilarTickets from './components/SimilarTickets';
import './styles/main.css'; // Import the main CSS file

function App() {
  const [ticket, setTicket] = useState(null);
  const [similarTickets, setSimilarTickets] = useState([]);
  const [submissionTime, setSubmissionTime] = useState(null);
  const [finalResponse, setFinalResponse] = useState(null);
  const [resolutionTime, setResolutionTime] = useState(null);

  const clearSession = () => {
    setTicket(null);
    setSimilarTickets([]);
    setSubmissionTime(null);
    setFinalResponse(null);
    setResolutionTime(null);
  };

  const formatResolutionTime = () => {
    if (!submissionTime || !resolutionTime) return "0";
    
    const diff = resolutionTime - submissionTime;
    const hours = Math.floor(diff / 3600000);
    const minutes = Math.floor((diff % 3600000) / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${seconds}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${seconds}s`;
    } else {
      return `${seconds}s`;
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="container header-content">
          <h1>Customer Ticket Resolver</h1>
          {ticket && (
            <button
              onClick={clearSession}
              className="btn btn-light"
            >
              New Ticket
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          {!ticket ? (
            <TicketForm 
              setTicket={setTicket} 
              setSimilarTickets={setSimilarTickets} 
              setSubmissionTime={setSubmissionTime} 
            />
          ) : (
            <div className="grid">
              {/* Left Column */}
              <div>
                <TicketDetails ticket={ticket} finalResponse={finalResponse} />
                
                {finalResponse && submissionTime && resolutionTime && (
                  <div className="card">
                    <h3 className="card-title">Resolution Information</h3>
                    <div className="resolution-box">
                      <div className="resolution-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                          <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                      </div>
                      <div>
                        <p className="mb-1">Ticket resolved in</p>
                        <p className="resolution-time">{formatResolutionTime()}</p>
                      </div>
                    </div>
                  </div>
                )}
                
                <SimilarTickets similarTickets={similarTickets} />
              </div>
              
              {/* Right Column */}
              <div>
                {!finalResponse && (
                  <AgentActions 
                    ticket={ticket} 
                    setTicket={setTicket} 
                    setFinalResponse={setFinalResponse} 
                    setResolutionTime={setResolutionTime} 
                  />
                )}
                
                {finalResponse && (
                  <div className="card">
                    <h3 className="card-title">Final Response</h3>
                    <div className="bg-success-light p-4 rounded border">
                      {finalResponse}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
      
      {/* Footer */}
      <footer className="footer">
        <div className="container">
          Customer Ticket Resolution System © {new Date().getFullYear()}
        </div>
      </footer>
    </div>
  );
}

export default App;