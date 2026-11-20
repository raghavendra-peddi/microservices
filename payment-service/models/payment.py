from pydantic import BaseModel, Field

class Payment(BaseModel):
    order_id: int = Field(..., description="The unique identifier for the payment")
    amount: float = Field(..., description="The amount of the payment")