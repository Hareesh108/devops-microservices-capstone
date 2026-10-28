
import pytest
from app import app, carts


@pytest.fixture
def client():
    app.config["TESTING"] = True
    carts.clear()

    with app.test_client() as client:
        yield client

    carts.clear()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_empty_cart(client):
    response = client.get("/cart/1")

    assert response.status_code == 200
    assert response.json["items"] == []


def test_add_item(client):
    response = client.post(
        "/cart/1/items",
        json={"product_id": 101, "quantity": 2},
    )

    assert response.status_code == 201
    assert response.json["items"] == [
        {"product_id": 101, "quantity": 2}
    ]


def test_add_same_item_increases_quantity(client):
    client.post(
        "/cart/1/items",
        json={"product_id": 101, "quantity": 2},
    )

    response = client.post(
        "/cart/1/items",
        json={"product_id": 101, "quantity": 3},
    )

    assert response.status_code == 201
    assert response.json["items"][0]["quantity"] == 5


def test_reject_invalid_quantity(client):
    response = client.post(
        "/cart/1/items",
        json={"product_id": 101, "quantity": 0},
    )

    assert response.status_code == 400


def test_remove_item(client):
    client.post(
        "/cart/1/items",
        json={"product_id": 101, "quantity": 1},
    )

    response = client.delete("/cart/1/items/101")

    assert response.status_code == 200
    assert response.json["items"] == []
