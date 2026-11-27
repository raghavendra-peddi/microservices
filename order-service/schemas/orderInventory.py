from pydantic import BaseModel, Field

class OrderInventoryCreate(BaseModel):
    name: str = Field(..., description="The name of the inventory item")
    quantity: int = Field(..., description="The quantity of the inventory item")
    description: str = Field(..., description="The description of the inventory item")
    price: float = Field(..., description="The price of the inventory item")
    currency: str = Field(..., description="The currency of the inventory item")

class OrderInventoryResponse(BaseModel):
    inventory_id: int = Field(..., description="The ID of the inventory item")
    name: str = Field(..., description="The name of the inventory item")
    quantity: int = Field(..., description="The quantity of the inventory item")
    description: str = Field(..., description="The description of the inventory item")
    price: float = Field(..., description="The price of the inventory item")
    currency: str = Field(..., description="The currency of the inventory item")

class OrderInventoryUpdate(BaseModel):
    inventory_id: int = Field(..., description="The ID of the inventory item")
    name: str = Field(..., description="The name of the inventory item")
    quantity: int = Field(..., description="The quantity of the inventory item")
    description: str = Field(..., description="The description of the inventory item")
    price: float = Field(..., description="The price of the inventory item")
    currency: str = Field(..., description="The currency of the inventory item")
