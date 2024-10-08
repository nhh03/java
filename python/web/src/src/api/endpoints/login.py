from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core import security
from src.core.config import settings
from src.api import deps
from src.db import crud
from src.db import schemas

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        user = crud.get_user(db, user_email=form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        else:
            user = crud.create_user(db, schemas.UserCreate(
                email=form_data.username,
                password=form_data.password
            ))
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.email,
            expires_delta=access_token_expires),
        "token_type": "bearer",
    }
