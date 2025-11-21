from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database for storing user accounts
db: Dict[str, Dict] = {
    "Owais": {"pin": "1234", "balance": 10000},
    "Danish": {"pin": "5678", "balance": 5000},
}

class AuthDetails(BaseModel):
    name: str
    pin_number: str

class TransferDetails(BaseModel):
    sender_name: str
    sender_pin: str
    recipient_name: str
    amount: float

@app.post("/authenticate")
async def authenticate(details: AuthDetails):
    """
    Authenticates a user and returns their account balance.
    """
    user = db.get(details.name)
    if not user or user["pin"] != details.pin_number:
        raise HTTPException(status_code=401, detail="Invalid name or PIN.")
    return {"name": details.name, "balance": user["balance"]}

@app.post("/bank-transfer")
async def bank_transfer(details: TransferDetails):
    """
    Transfers a specified amount from one user to another.
    """
    sender = db.get(details.sender_name)
    recipient = db.get(details.recipient_name)

    if not sender or sender["pin"] != details.sender_pin:
        raise HTTPException(status_code=401, detail="Invalid sender name or PIN.")
    
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found.")

    if details.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive.")

    if sender["balance"] < details.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    # Perform the transfer
    sender["balance"] -= details.amount
    recipient["balance"] += details.amount

    return {
        "message": f"Successfully transferred {details.amount} from {details.sender_name} to {details.recipient_name}.",
        "sender_new_balance": sender["balance"],
        "recipient_new_balance": recipient["balance"]
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the Simple Banking API!"}
