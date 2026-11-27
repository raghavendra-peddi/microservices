from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from models.customer import Customer
from schemas.customer import CustomerLogin
from pwdlib import PasswordHash
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from datetime import datetime, timedelta, timezone
from config import settings

router = APIRouter()

@router.get("/")
def root():
    return {
        "status": "auth-service is running",
    }

@router.post("/login")
async def auth_login(customer_login: CustomerLogin, session: AsyncSession = Depends(get_db)):
    try:
        customer = select(Customer).where(Customer.email == customer_login.email)
        result = await session.execute(customer)
        customer = result.scalar_one_or_none()
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        password_hash = PasswordHash.recommended()
        if not password_hash.verify(customer_login.password, customer.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Generate JWT token
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub": str(customer.customer_id),
            "email": customer.email,
            "exp": expire,
            "role": customer.role
        }
        token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return {
            "status": "login successful",
            "token": token,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

@router.put("/update-password")
async def update_password(
    customer_id: int,
    password: str,
    session: AsyncSession = Depends(get_db),
):
    try:
        ## once email service is setup.. add one time password verification here
        customer = await session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        password_hash = PasswordHash.recommended()
        hashed_password = password_hash.hash(password)
        customer.password_hash = hashed_password

        await session.commit()
        await session.refresh(customer)
        return {
            "status": "ok",
            "message": "Password updated successfully"
        }
    except Exception as e:
        logger.error(f"Error updating password: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update password")

