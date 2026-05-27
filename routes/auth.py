from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from typing import Annotated, Literal

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from bd import get_users
from objects import User

router = APIRouter(prefix="/auth", tags=["auth"])

# Define donde Swagger buscará el token (el endpoint de login)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "mi clave super super secreta y segura"
ALGORITHM = "HS256"

def create_token(data: dict, type: Literal["Access", "Refresh"], expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + expires_delta
    to_encode.update({"iat": now, "exp": expire, "type": type})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def set_cookie(response: Response, data: dict, expires_delta: timedelta = timedelta(days=15)):
    response.set_cookie(
        key="session_token",
        value=create_token(data, "Refresh", expires_delta),
        httponly=True,                                  # <--- Clave: JavaScript no puede robarlo
        secure=False,                                   # <--- Cambiar a True en producción (requiere HTTPS)
        samesite="lax",                                 # <--- Protege contra ataques CSRF
        max_age = int(expires_delta.total_seconds()),   # <--- Duración en segundos (15 dias)
    )

def set_access(response: Response, data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    token = create_token(data, "Access", expires_delta)
    response.headers["Authorization"] = token
    response.headers["WWW-Authenticate"] = token

@router.post("/login", status_code=HTTPStatus.ACCEPTED)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, users: Annotated[list[User], Depends(get_users)]):
    data_token = None

    for u in users:
        if u.name.lower() == form_data.username.lower() and u.password == form_data.password:
            data_token = {"id": u.id, "name": u.name}

    if not data_token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

    set_cookie(response, data_token)
    set_access(response, data_token)

    #return {"ok": True, "message": "Access accept"}

    return {"access_token": create_token(data_token, "Access"), "token_type": "bearer"}

@router.post("/logout", status_code=HTTPStatus.OK)
def logout(response: Response):
    response.delete_cookie("session_token")
    return {"ok": True, "message": "Logout"}

@router.post("/refresh", status_code=HTTPStatus.OK)
def refresh(response: Response, session_token: Annotated[str | None, Cookie()] = None):
    try:
        if not session_token:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="No hay cookie")

        data = jwt.decode(session_token, SECRET_KEY, ALGORITHM)

        if data.get("id") is None or data.get("name") is None:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Token incorrecto", headers={"WWW-Authenticate": "Bearer"})

        data_token = {"id": data.get("id"), "name": data.get("name")}

        set_cookie(response, data_token)
        set_access(response, data_token)

        # return {"ok": True, "message": "Access refresh"}
        return {"access_token": create_token(data_token, "Access"), "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Token caducado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)

def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        data = jwt.decode(token, SECRET_KEY, ALGORITHM)

        if data.get("id") is None or data.get("name") is None:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Token incorrecto", headers={"WWW-Authenticate": "Bearer"})

        return {"id": data.get("id"), "name": data.get("name")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Token caducado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)

