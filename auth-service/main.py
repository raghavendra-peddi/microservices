from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from database import engine, Base
from routes import auth_router
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
    root_path="/auth"
)

# Include auth routes
app.include_router(auth_router)