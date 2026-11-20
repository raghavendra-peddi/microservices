from fastapi import FastAPI, HTTPException
from models.order import Order
import httpx

app = FastAPI(root_path="/orders")

@app.get("/")
def root():
    return {"status": "order-service is running"}

@app.post("/orders")
def create_order(order: Order):
    if order.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid order amount")
    if order.id == 501:
        raise HTTPException(status_code=500, detail="Invalid order ID")
    try:
        paymentResponse = httpx.post("http://payment-service:8000/payments", json={"order_id": order.id, "amount": order.amount}, timeout=3.0)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Payment service timeout")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Payment service unavailable")
    
    if paymentResponse.status_code == 400:
        raise HTTPException(status_code=400, detail="Payment service rejected the request")
    if paymentResponse.status_code >= 400:
        raise HTTPException(status_code=paymentResponse.status_code, detail="Payment service error")
    
    return paymentResponse.json()