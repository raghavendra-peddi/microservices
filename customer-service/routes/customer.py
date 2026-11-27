from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from pwdlib import PasswordHash
from dependencies import get_current_user, verify_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
protected_router = APIRouter(
    dependencies=[Depends(verify_token)],
)

@router.get("/")
def root():
    return {
        "status": "customer-service is running",
    }


@protected_router.get("/customers")
async def get_customers(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Access token data
        user_id = int(current_user.get("sub"))
        user_role = current_user.get("role")

        count_query = select(func.count(Customer.customer_id))
        total = await session.scalar(count_query)
        
        if user_role == "admin":
            query = select(Customer).offset(skip).limit(limit)
        else:
            query = select(Customer).where(Customer.customer_id == user_id).offset(skip).limit(limit)

        result = await session.execute(query)
        customers = result.scalars().all()

        return {
            "status": "ok",
            "data": [
                {
                    "id": c.customer_id,
                    "name": c.name,
                    "email": c.email,
                    "phone": c.phone,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                }
                for c in customers
            ],
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch customers")


@protected_router.get("/customer/{customer_id}")
async def get_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Access token data
        user_id = int(current_user.get("sub"))
        user_role = current_user.get("role")

        # Optional: Only allow users to view their own data unless they're an admin
        if user_role != "admin" and customer_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to view this customer")

        customer = await session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {
            "status": "ok",
            "data": CustomerResponse.model_validate(customer).model_dump()
        }
    except Exception as e:
        logger.error(f"Error fetching customer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch customer")


@router.post("/create-customer")
async def create_customer(customer_data: CustomerCreate, session: AsyncSession = Depends(get_db)):
    try:
        # Check if customer with this email already exists
        existing_customer = select(Customer).where(Customer.email == customer_data.email)
        result = await session.execute(existing_customer)
        existing_customer = result.scalar_one_or_none()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
        
        password_hash = PasswordHash.recommended()
        hashed_password = password_hash.hash(customer_data.password)
        customer = Customer(
            name=customer_data.name,
            email=customer_data.email,
            phone=customer_data.phone,
            password_hash=hashed_password
        )
        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return {
            "status": "ok",
            "data": CustomerResponse.model_validate(customer).model_dump()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create customer")


@protected_router.put("/update-customer/{customer_id}")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Access token data
        user_id = int(current_user.get("sub"))
        user_role = current_user.get("role")

        # Only allow users to update their own data unless they're an admin
        if user_role != "admin" and customer_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this customer")

        customer = await session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        if customer_data.name:
            customer.name = customer_data.name
        if customer_data.email:
            customer.email = customer_data.email
        if customer_data.phone:
            customer.phone = customer_data.phone

        await session.commit()
        await session.refresh(customer)
        return {
            "status": "ok",
            "data": CustomerResponse.model_validate(customer).model_dump()
        }
    except Exception as e:
        logger.error(f"Error updating customer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update customer")


@protected_router.delete("/delete-customer/{customer_id}")
async def delete_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Access token data
        user_id = int(current_user.get("sub"))
        user_role = current_user.get("role")

        # Only allow users to delete their own data unless they're an admin
        if user_role != "admin" and customer_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this customer")

        customer = await session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        await session.delete(customer)
        await session.commit()
        return {
            "status": "ok",
            "message": "Customer deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting customer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete customer")
