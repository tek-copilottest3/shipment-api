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


@app.post("/shipments", status_code=201)
def create_shipment(request: ShipmentRequest):
    if request.shipment_id in SHIPMENT_STORE:
        raise HTTPException(status_code=409, detail="Shipment already exists")

    SHIPMENT_STORE[request.shipment_id] = request.status
    return {"shipment_id": request.shipment_id, "status": request.status}


@app.get("/shipments")
def list_shipments():
    return [
        {"shipment_id": shipment_id, "status": status}
        for shipment_id, status in SHIPMENT_STORE.items()
    ]
