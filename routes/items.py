from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from bd import get_db
from objects import Db, Item
from routes.auth import get_current_user

router = APIRouter(prefix="/items", tags=["items"])

async def common_parameters(q: Annotated[str | None, Query(description="Parte del nombre del item", min_length=1, max_length=50, pattern="^[a-zA-Z0-9 ]+$")] = None,
                            skip: Annotated[int, Query(description="Desde que item empezar", ge=0, le=4)] = 0,
                            limit: Annotated[int, Query(description="Cuantos items sacar", ge=0, le=100)] = 100):
    print(q, skip, limit)
    return {"q": q, "skip": skip, "limit": limit}

@router.get("/", response_model=list[Item])
def get_items(db: Annotated[dict, Depends(get_db)]):
    return db.items

@router.get("/search", status_code=HTTPStatus.OK, response_model=list[Item], responses={204: {"description": "No se ha encontrado contenido que coincida con la busqueda"}, 500: {"description": "Error interno al conectar con el servidor de datos"}})
def search_item(commons: Annotated[dict, Depends(common_parameters)], db: Annotated[Db, Depends(get_db)]):
    items = [item for item in db.items if not commons.get("q") or commons.get("q", "").lower() in item.name.lower()]
    return items[commons.get("skip"): commons.get("skip", 0) + commons.get("limit")]

@router.get("/{item_id}", status_code=HTTPStatus.OK, response_model=Item)
def get_item(item_id: Annotated[int, Path(description="Id del item", ge=1, le=1000)], db: Annotated[Db, Depends(get_db)]):
    for i in db.items:
        if i.id == item_id:
            return i
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Item not found")

@router.post("/", status_code=HTTPStatus.CREATED, response_model=Item)
def create_item(item: Item, user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if user.get("id") != 0:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")
    if item.id in [i.id for i in db.items]:
        raise HTTPException(HTTPStatus.CONFLICT, detail="The ID is exists in database")
    db.items.append(item)
    return item

@router.delete("/{item_id}", status_code=HTTPStatus.OK)
def delete_item(item_id: Annotated[int, Path(description="Id del item", ge=1, le=1000)], user: Annotated[dict, Depends(get_current_user)], db: Annotated[Db, Depends(get_db)]):
    if user.get("id") != 0:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized user")

    for i in db.items:
        if i.id == item_id:
            db.items.remove(i)
            return {"ok": True, "message": "Item deleted"}
    return {"ok": False, "message": "Item not found"}
