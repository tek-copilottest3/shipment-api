from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Shipment API")

# In-memory shipment store
SHIPMENT_STORE = {
    "SHP001": "In Transit",
    "SHP002": "Delivered",
    "SHP003": "Pending Pickup",
    "SHP004": "Out for Delivery",
    "SHP005": "Returned to Sender",
}


class ShipmentRequest(BaseModel):
    shipment_id: str
    status: str


@app.get("/")
def root():
    return {"message": "Shipment API is running"}


@app.get("/status/{shipment_id}")
def get_status(shipment_id: str):
    if shipment_id not in SHIPMENT_STORE:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"shipment_id": shipment_id, "status": SHIPMENT_STORE[shipment_id]}


# TODO: Add POST /shipments endpoint here.
# - Accept a ShipmentRequest body (shipment_id and status).
# - If shipment_id already exists in SHIPMENT_STORE, return HTTP 409.
# - On success, add to SHIPMENT_STORE and return the created shipment with HTTP 201.
