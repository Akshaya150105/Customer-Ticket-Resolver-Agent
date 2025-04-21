'''
This defines the schemas , including the request and response models.
It uses Pydantic for data validation and serialization.
'''
from pydantic import BaseModel
from typing import Optional, List

class TicketCreate(BaseModel):
    issue_description: str

    class Config:
        schema_extra = {
            "example": {
                "issue_description": "poor network in my area"
            }
        }

class TicketResponse(BaseModel):
    ticket_id: str
    issue_description: str
    category: str  # Predicted category
    confirmed_category: Optional[str] = None  # Agent-confirmed category
    draft_response: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "ticket_id": "JIO-N1234",
                "issue_description": "poor network in my area",
                "category": "Network",
                "confirmed_category": "Network",
                "draft_response": "Please check your signal booster installation."
            }
        }

class SimilarTicket(BaseModel):
    ticket_id: str
    issue_description: str
    resolution: str
    category: str
    similarity_score: float

class SimilarTicketsResponse(BaseModel):
    ticket_id: str
    similar_tickets: List[SimilarTicket]

class ApprovalRequest(BaseModel):
    final_response: str
class CategoryApprovalRequest(BaseModel):
    confirmed_category: str