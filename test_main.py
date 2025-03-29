from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_single_product():
    response = client.get("/getSingleProduct", params={"product_id": 1})
    assert response.status_code in [200, 404]


def test_get_all_products():
    response = client.get("/getAll")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_new_product():
    product = {
        "ProductID": 999,
        "Name": "Test Product",
        "UnitPrice": 19.99,
        "StockQuantity": 50,
        "Description": "A test product.",
    }
    response = client.post("/addNew", json=product)
    assert response.status_code in [200, 400]


def test_delete_product():
    response = client.delete("/deleteOne", params={"product_id": 999})
    assert response.status_code in [200, 404]


def test_starts_with():
    response = client.get("/startsWith", params={"letter": "T"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_paginate():
    response = client.get("/paginate", params={"start_id": 1, "end_id": 10})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_convert_to_euro():
    response = client.get("/convert", params={"product_id": 1})
    assert response.status_code in [200, 404]
