from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from config import settings
from database import engine, Base
from routes.customer import router as customer_router
from routes.customer import protected_router as customer_protected_router
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
       await conn.execute(text("SELECT 1"))
    logger.info("Database connection verified")
    
    yield
    
    await engine.dispose()
    logger.info("Database connection closed")

app = FastAPI(
    lifespan=lifespan,
    title="Customer Service API",
    root_path="/customers"
)

# Include customer routes
app.include_router(customer_router)
app.include_router(customer_protected_router)
