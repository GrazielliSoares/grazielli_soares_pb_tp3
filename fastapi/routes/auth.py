
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pwdlib import PasswordHash

from database import get_session
from limiter import limiter
from models.database_models import User
from models.schemas import Token
from security.authentication import create_access_token

router = APIRouter()
password_hash = PasswordHash.recommended()


@router.post("/auth/token", response_model=Token)
@limiter.limit("10/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    usuario = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if usuario is None or not password_hash.verify(
        form_data.password,
        usuario.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": usuario.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
