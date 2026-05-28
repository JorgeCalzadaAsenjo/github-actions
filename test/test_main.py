from http import HTTPStatus
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)

def test_leer_init():
    respuesta = cliente.get("/")
    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json() == {"status": "Service is up", "OK": True}

def test_leer_ok():
    respuesta = cliente.get("/ok")
    assert respuesta.status_code == HTTPStatus.CREATED

def test_leer_error():
    respuesta = cliente.get("/error")
    assert respuesta.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

def test_escribir_init():
    respuesta = cliente.post("/")
    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json() == {"status": "OK", "OK": True}
