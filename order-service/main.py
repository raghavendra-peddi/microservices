from fastapi import FastAPI
from routes.order import router as order_router
from routes.order import protected_router as order_protected_router
from contextlib import asynccontextmanager
from database import engine
from sqlalchemy import text
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

app = FastAPI(title="Order Service API", root_path="/orders", lifespan=lifespan)

app.include_router(order_router)
app.include_router(order_protected_router)
