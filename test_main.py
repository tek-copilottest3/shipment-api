import pytest
from fastapi.testclient import TestClient
from main import SHIPMENT_STORE, app

client = TestClient(app)


def test_create_new_shipment():
    response = client.post("/shipments", json={
        "shipment_id": "SHP999",
        "status": "Pending Pickup"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["shipment_id"] == "SHP999"
    assert data["status"] == "Pending Pickup"


def test_create_duplicate_shipment():
    response = client.post("/shipments", json={
        "shipment_id": "SHP001",
        "status": "In Transit"
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "Shipment already exists"


def test_list_shipments_returns_all_entries():
    expected_shipments = {
        (shipment_id, status) for shipment_id, status in SHIPMENT_STORE.items()
    }

    response = client.get("/shipments")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    actual_shipments = {
        (item["shipment_id"], item["status"]) for item in response.json()
    }
    assert actual_shipments == expected_shipments
