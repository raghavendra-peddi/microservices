from pydantic import BaseModel, Field

class Order(BaseModel):
    id: int = Field(..., description="The unique identifier for the order")
    amount: float = Field(..., description="The amount of the order")