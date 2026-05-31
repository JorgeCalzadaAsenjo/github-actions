from http import HTTPStatus


def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)

def test_get_item_by_id(client):
    response = client.get("/items/0")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Foo"

def test_get_item_negatve_id(client):
    response = client.get("/items/-1")
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_create_item_unauthorized(client):
    new_item = {"id": 10, "name": "New Item", "price": 10.5, "is_offer": False}
    response = client.post("/items/", json=new_item)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_create_item(authorized_client):
    new_item = {"id": 10, "name": "New Item", "price": 10.5, "is_offer": False}
    response = authorized_client.post("/items/", json=new_item)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["name"] == "New Item"

def test_delete_item_unauthorized(client):
    response = client.delete("/items/1")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_delete_item(authorized_client):
    response = authorized_client.delete("/items/1")
    assert response.status_code == HTTPStatus.OK

def test_search_items(client):
    response = client.get("/items/search?q=Foo")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Foo"

def test_search_items_no_results(client):
    response = client.get("/items/search?q=NonExistent")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
