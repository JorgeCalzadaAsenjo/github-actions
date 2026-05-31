from http import HTTPStatus


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
