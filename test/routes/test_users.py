from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)

# Fixture que obtiene un token y devuelve un cliente autenticado
@pytest.fixture
def authorized_client(client):
    # 1. Simulas el login para obtener el token real (o usas uno de prueba)
    response = client.post("/auth/login", data={"username": "admin", "password": "01234"})
    token = response.json()["access_token"]

    # 2. Inyectas el token en las cabeceras del cliente
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

def test_get_users_unauthorized(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_users(authorized_client):
    response = authorized_client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)

def test_get_user_by_id_unauthorized(client):
    response = client.get("/users/0")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_user_by_id(authorized_client):
    response = authorized_client.get("/users/0")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Admin"

def test_get_user_not_found(authorized_client):
    response = authorized_client.get("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
