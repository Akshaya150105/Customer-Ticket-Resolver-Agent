from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SessionLocal, NewTicket
from .schemas import TicketCreate, TicketResponse
from .classification import classify_ticket
import uuid
from fastapi import Depends
import logging
from .similarity import get_similar_tickets, initialize_index

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Customer Ticket Resolver Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize index on startup
@app.on_event("startup")
async def startup_event():
    initialize_index()

@app.post("/submit_ticket", response_model=TicketResponse)
async def submit_ticket(ticket: TicketCreate, db=Depends(get_db)):
    """
    Receive and store a new ticket query with classification and generate a draft response.
    """
    try:
        logger.info(f"Received ticket: {ticket.issue_description}")
        ticket_id = f"JIO-N{uuid.uuid4().hex[:4].upper()}"
        logger.info(f"Generated ticket_id: {ticket_id}")
        category = classify_ticket(ticket.issue_description)
        if category is None:
            raise ValueError("Classification failed: No category returned")
        logger.info(f"Classified category: {category}")
        db_ticket = NewTicket(
            ticket_id=ticket_id,
            issue_description=ticket.issue_description,
            status="Pending",
            category=category
        )
        db.add(db_ticket)
        db.commit()
        logger.info(f"Ticket stored in DB: {ticket_id}")
        db.refresh(db_ticket)

        # Generate draft response from similar tickets
        similar_tickets = get_similar_tickets(ticket.issue_description, top_k=1)
        logger.info(f"Similar tickets retrieved: {similar_tickets}")
        draft_response = None
        if similar_tickets and 'resolution' in similar_tickets[0] and similar_tickets[0]['resolution']:
            draft_response = similar_tickets[0]['resolution']
            logger.info(f"Draft response generated: {draft_response}")
        else:
            draft_response = "No past resolution available. Please investigate further or contact support."
            logger.warning("No valid resolution found in similar tickets.")

        response_data = {
            "ticket_id": ticket_id,
            "issue_description": ticket.issue_description,
            "category": category,
            "draft_response": draft_response
        }
        logger.info(f"Returning response: {response_data}")
        return response_data
    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error submitting ticket: {str(e)}")

@app.get("/similar_tickets/{ticket_id}")
async def get_similar_tickets_endpoint(ticket_id: str, db=Depends(get_db)):
    """
    Retrieve similar tickets based on the issue_description of the given ticket_id.
    """
    try:
        # Fetch the ticket to get its issue_description
        ticket = db.query(NewTicket).filter(NewTicket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        logger.info(f"Found ticket: {ticket_id}, issue: {ticket.issue_description}")
        
        # Get similar tickets using the ticket's issue_description
        similar_tickets = get_similar_tickets(ticket.issue_description, top_k=3)
        logger.info(f"Returning similar tickets: {similar_tickets}")
        return similar_tickets
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching similar tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching similar tickets: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)