from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.db_session.db_engine import get_session
from app.schemas.token_schema import Token
from app.schemas.user_schema import User
from app.security.hashing import create_access_token, verify_password

ACCESS_TOKEN_EXPIRE_MINUTES = 3000000

router = APIRouter(prefix="/api")


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    query = select(User).where(User.email == form_data.username)
    user: User | None = session.exec(query).first()

    if user is None:
        raise_401_exception()

    assert user is not None

    if not verify_password(form_data.password, user.password):
        raise_401_exception()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


def raise_401_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
