from pydantic import BaseModel
from typing import Optional, List
# Input schema (what the client sends)
class TicketCreate(BaseModel):
    issue_description: str

    class Config:
        schema_extra = {
            "example": {
                "issue_description": "poor network in my area"
            }
        }

# Response schema (what the backend returns)
class TicketResponse(BaseModel):
    ticket_id: str
    issue_description: str
    category: str
    draft_response: str | None = None  # Optional draft response

    class Config:
        schema_extra = {
            "example": {
                "ticket_id": "JIO-N1234",
                "issue_description": "poor network in my area",
                "category": "Network",
                "draft_response": "Please check your signal booster installation."
            }
        }

class SimilarTicket(BaseModel):
    ticket_id: str
    issue_description: str
    resolution: str
    category: str
    similarity_score: float

class TicketResponse(TicketCreate):
    ticket_id: str
    category: str

class SimilarTicketsResponse(BaseModel):
    ticket_id: str
    similar_tickets: List[SimilarTicket]

    