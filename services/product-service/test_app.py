
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_all_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json) == 3


def test_get_existing_product(client):
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json["name"] == "Laptop"


def test_get_missing_product(client):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json["error"] == "Product not found"
