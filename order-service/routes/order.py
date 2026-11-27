from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from dependencies import verify_token, get_current_user
from schemas.orderInventory import OrderInventoryCreate, OrderInventoryResponse
from models.orderInventory import OrderInventory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()
protected_router = APIRouter(dependencies=[Depends(verify_token)])

@router.get("/")
def root():
    return {"status": "order-service is running"}


@protected_router.post("/order-inventory")
async def create_order_inventory(
    order_data: OrderInventoryCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create orders")

    order = OrderInventory(
        name=order_data.name,
        quantity=order_data.quantity,
        description=order_data.description,
        price=order_data.price
    )

    session.add(order)
    await session.commit()
    await session.refresh(order)

    return {"status": "order created", "order": order}
    
@protected_router.get("/order-inventory")
async def get_order_inventory(
    inventory_id: int = None,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can get orders")

    if inventory_id:
        order = await session.get(OrderInventory, inventory_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return {"status": "order found", "order": order}

    # Get all orders
    result = await session.execute(select(OrderInventory))
    orders = result.scalars().all()
    return {"status": "orders found", "orders": orders}
    