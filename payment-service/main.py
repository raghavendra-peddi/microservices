from fastapi import FastAPI, HTTPException
from models.payment import Payment

app = FastAPI(root_path="/payments")

@app.get("/")
def root():
    return {"status": "payment-service is running"}


@app.post("/payments")
def create_payment(payment: Payment):
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid payment amount")
    return {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "success"
    }