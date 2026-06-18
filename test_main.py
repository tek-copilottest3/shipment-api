import pytest
from fastapi.testclient import TestClient
from main import app

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
