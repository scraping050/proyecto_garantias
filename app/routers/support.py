from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.support import SupportTicket
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/api/support",
    tags=["support"],
    responses={404: {"description": "Not found"}},
)

class TicketCreate(BaseModel):
    subject: str
    message: str

@router.post("/contact")
async def create_ticket(
    ticket: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_ticket = SupportTicket(
        user_id=current_user.id,
        subject=ticket.subject,
        message=ticket.message,
        status="OPEN"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    return {"message": "Ticket created successfully", "id": new_ticket.id}
