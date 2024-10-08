from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api import deps
from src.db import crud
from src.db import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve tickets.
    """
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets


@router.get("/{id}", response_model=schemas.Ticket)
def read_ticket(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get a ticket by ID.
    """
    ticket = crud.get_ticket(db=db, ticket_id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Item not found")
    return ticket