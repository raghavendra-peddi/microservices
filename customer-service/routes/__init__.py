from .customer import router as customer_router
from .customer import protected_router as customer_protected_router

__all__ = ["customer_router", "customer_protected_router"]
