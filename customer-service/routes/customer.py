from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def root():
    return {
        "status": "customer-service is running",
    }


@router.get("/customers")
async def get_customers(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_db)):
    try:
        count_query = select(func.count(Customer.customer_id))
        total = await session.scalar(count_query)
        
        query = select(Customer).offset(skip).limit(limit)
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


@router.get("/customer/{customer_id}")
async def get_customer(customer_id: int, session: AsyncSession = Depends(get_db)):
    try:
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
        customer = Customer(name=customer_data.name, email=customer_data.email, phone=customer_data.phone)
        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return {
            "status": "ok",
            "data": CustomerResponse.model_validate(customer).model_dump()
        }
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create customer")


@router.put("/update-customer/{customer_id}")
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: AsyncSession = Depends(get_db)):
    try:
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


@router.delete("/delete-customer/{customer_id}")
async def delete_customer(customer_id: int, session: AsyncSession = Depends(get_db)):
    try:
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
