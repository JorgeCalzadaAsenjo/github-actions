from http import HTTPStatus


def test_login_success(client):
    response = client.post(
        "/auth/login", data={"username": "Admin", "password": "01234"},
    )
    assert response.status_code == HTTPStatus.ACCEPTED
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login", data={"username": "Admin", "password": "wrongpassword"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"ok": True, "message": "Logout"}

def test_refresh_token_no_cookie(client):
    response = client.post("/auth/refresh")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_refresh_token_success(client):
    # First login to get the session cookie
    login_response = client.post(
        "/auth/login", data={"username": "Admin", "password": "01234"},
    )
    assert login_response.status_code == HTTPStatus.ACCEPTED

    # Use the cookie from the login response to refresh
    refresh_response = client.post("/auth/refresh")
    assert refresh_response.status_code == HTTPStatus.OK
    assert "access_token" in refresh_response.json()
