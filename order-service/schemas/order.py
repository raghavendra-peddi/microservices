from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    customer_id: int = Field(..., description="The ID of the customer")
    amount: float = Field(..., description="The amount of the order")
    status: str = Field(..., description="The status of the order")

class OrderResponse(BaseModel):
    order_id: int = Field(..., description="The unique identifier for the order")
    customer_id: int = Field(..., description="The ID of the customer")
    amount: float = Field(..., description="The amount of the order")
    status: str = Field(..., description="The status of the order")
    created_at: str = Field(..., description="The creation timestamp of the order")
    updated_at: str = Field(..., description="The last update timestamp of the order")
    order_items: list = Field(..., description="The items in the order")


class OrderUpdate(BaseModel):
    order_id: int = Field(..., description="The unique identifier for the order")
    status: str = Field(..., description="The status of the order")
    order_items: list = Field(..., description="The items in the order")