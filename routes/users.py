from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from bd import get_db
from objects import Db, User
from routes.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(username: Annotated[dict, Depends(get_current_user)]):
    return {**username}

@router.get("/me/items")
def get_me_items(user: Annotated[dict, Depends(get_current_user)]):
    return {"user": user.get("name"), "items": []}

@router.get("/users")
def get_users(user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if user.get("id") == 0:
        return db.users
    raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

@router.get("/admins")
def get_admins(user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if user.get("id") == 0:
        return [u for u in db.users if u.id > 0]
    raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

@router.get("/{user_id}")
def get_user_by_id(user_id: int, user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if user.get("id") != 0:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

    for u in db.users:
        if u.id == user_id:
            return u
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int, user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if user.get("id") != 0:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

    for u in db.users:
        if u.id == user_id:
            db.users.remove(u)
            return {"ok": True, "message": "User deleted"}
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")

@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(new_user: Annotated[User, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if new_user.id != 0:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

    if any(u.id == new_user.id for u in db.users):
        raise HTTPException(HTTPStatus.CONFLICT, detail="User already exists")

    db.users.append(new_user)
    return new_user

@router.put("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, new_user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if new_user.get("id") != 0:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

    for index, u in enumerate(db.users):
        if u.id == user_id:
            # En una implementación real, aquí se actualizaría el objeto con los datos del body
            # Por simplicidad, devolvemos el usuario encontrado
            return db.users[index]
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")
