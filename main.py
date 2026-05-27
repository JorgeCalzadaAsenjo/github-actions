from dataclasses import dataclass
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from routes import auth_router, item_router, user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(item_router)
app.include_router(user_router)

@app.get("/", status_code=HTTPStatus.OK, tags=["init"])
def get_init():
    return {"status": "Service is up", "OK": True}

@app.get("/ok", status_code=HTTPStatus.CREATED, tags=["init"])
def get_ok():
    return {"status": "Service is up", "OK": True}

@app.get("/error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR, tags=["init"])
def get_error():
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@app.post("/", status_code=HTTPStatus.OK, tags=["init"])
def post_init():
    return {"status": "OK", "OK": True}
