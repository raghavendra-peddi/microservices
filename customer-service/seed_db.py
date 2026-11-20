import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, Base
from models.customer import Customer


async def seed_database():
    """Seed the database with sample customer data."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with SessionLocal() as session:
        # Check if customers already exist
        from sqlalchemy import select, func
        count_query = select(func.count(Customer.id))
        total = await session.scalar(count_query)
        
        if total > 0:
            print(f"Database already has {total} customers. Skipping seed.")
            return
        
        # Create sample customers
        customers = [
            Customer(
                name="John Doe",
                email="john.doe@example.com",
                phone="+1-555-0101"
            ),
            Customer(
                name="Jane Smith",
                email="jane.smith@example.com",
                phone="+1-555-0102"
            ),
            Customer(
                name="Bob Johnson",
                email="bob.johnson@example.com",
                phone="+1-555-0103"
            ),
            Customer(
                name="Alice Williams",
                email="alice.williams@example.com",
                phone="+1-555-0104"
            ),
            Customer(
                name="Charlie Brown",
                email="charlie.brown@example.com",
                phone="+1-555-0105"
            ),
        ]
        
        session.add_all(customers)
        await session.commit()
        
        print(f"Successfully seeded {len(customers)} customers into the database.")


if __name__ == "__main__":
    asyncio.run(seed_database())
