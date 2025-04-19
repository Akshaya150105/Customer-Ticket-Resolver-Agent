from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SessionLocal, NewTicket
from .schemas import TicketCreate, TicketResponse
from .classification import classify_ticket
import uuid
from fastapi import Depends
import logging
from .similarity import get_similar_tickets, initialize_index
from datetime import datetime
from pydantic import BaseModel

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
            category=category,
            draft_resolution=None
        )
        db.add(db_ticket)
        db.commit()
        logger.info(f"Ticket stored in DB: {ticket_id}")
        db.refresh(db_ticket)

        similar_tickets = get_similar_tickets(ticket.issue_description, top_k=1)
        logger.info(f"Similar tickets retrieved: {similar_tickets}")
        draft_response = None
        if similar_tickets and 'resolution' in similar_tickets[0] and similar_tickets[0]['resolution']:
            draft_response = similar_tickets[0]['resolution']
            db_ticket.draft_resolution = draft_response
            db.commit()
            logger.info(f"Draft resolution stored: {draft_response}")
        else:
            draft_response = "No past resolution available. Please investigate further or contact support."
            db_ticket.draft_resolution = draft_response
            db.commit()
            logger.warning("No valid resolution found in similar tickets. Using fallback.")

        if draft_response is None:
            draft_response = "Unable to generate draft response. Please check ticket data or database."
            db_ticket.draft_resolution = draft_response
            db.commit()
            logger.error("Draft response was None, forcing fallback.")

        response_data = {
            "ticket_id": ticket_id,
            "issue_description": ticket.issue_description,
            "category": category,
            "draft_response": draft_response
        }
        if "draft_response" not in response_data:
            logger.critical("Critical error: draft_response missing in response_data before return")
            raise HTTPException(status_code=500, detail="Internal server error: draft_response missing")
        logger.info(f"Final response before return: {response_data}")
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
        ticket = db.query(NewTicket).filter(NewTicket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        logger.info(f"Found ticket: {ticket_id}, issue: {ticket.issue_description}")
        
        similar_tickets = get_similar_tickets(ticket.issue_description, top_k=3)
        logger.info(f"Returning similar tickets: {similar_tickets}")
        return similar_tickets
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching similar tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching similar tickets: {str(e)}")

# Updated endpoint to accept final_response in the request body
class ApprovalRequest(BaseModel):
    final_response: str

@app.put("/approve_ticket/{ticket_id}")
async def approve_ticket(ticket_id: str, approval: ApprovalRequest, db=Depends(get_db)):
    """
    Approve and update the ticket with final resolution and resolution time.
    """
    try:
        ticket = db.query(NewTicket).filter(NewTicket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        logger.info(f"Approving ticket: {ticket_id}")

        if ticket.submission_time:
            resolution_duration = datetime.now() - ticket.submission_time
            resolution_hours = str(resolution_duration.total_seconds() / 3600)
        else:
            resolution_hours = "0.0"
            logger.warning("Submission time not found, using default resolution time.")

        ticket.final_resolution = approval.final_response
        ticket.status = "Resolved"
        ticket.resolution_time_hours = resolution_hours
        db.commit()
        logger.info(f"Ticket updated: {ticket_id}, final_resolution: {approval.final_response}, resolution_time_hours: {resolution_hours}")

        return {"message": "Ticket approved and updated", "ticket_id": ticket_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error approving ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error approving ticket: {str(e)}")
# New endpoint for category approval
class CategoryApprovalRequest(BaseModel):
    confirmed_category: str

@app.put("/approve_category/{ticket_id}")
async def approve_category(ticket_id: str, approval: CategoryApprovalRequest, db=Depends(get_db)):
    """
    Approve and update the ticket with the confirmed category.
    """
    try:
        ticket = db.query(NewTicket).filter(NewTicket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        logger.info(f"Approving category for ticket: {ticket_id}")

        ticket.confirmed_category = approval.confirmed_category
        db.commit()
        logger.info(f"Category updated: {ticket_id}, confirmed_category: {approval.confirmed_category}")

        return {"message": "Category approved and updated", "ticket_id": ticket_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error approving category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error approving category: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)