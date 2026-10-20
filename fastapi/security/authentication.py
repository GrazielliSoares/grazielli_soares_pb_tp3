
import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from database import get_session
from models.database_models import User
from sqlmodel import select

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict):
    if not SECRET_KEY:
        raise RuntimeError("Configure a variável JWT_SECRET_KEY.")

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if not SECRET_KEY:
        raise RuntimeError("Configure a variável JWT_SECRET_KEY.")

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if not isinstance(username, str) or not username:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    usuario = session.exec(
        select(User).where(User.username == username)
    ).first()

    if usuario is None:
        raise credentials_exception

    return usuario
