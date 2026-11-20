# Database Connection Troubleshooting

## Issue
`ConnectionRefusedError: [Errno 111] Connection refused` - The application cannot connect to PostgreSQL.

## Solution

### Step 1: Start PostgreSQL Container
```bash
cd /Users/rpeddi987@cable.comcast.com/workspace/Python/microservices
docker-compose up -d postgres
```

Verify it's running:
```bash
docker-compose ps
```

You should see `microservices-postgres-1` with status `Up`.

### Step 2: Configure .env File

The `.env` file must contain the correct DATABASE_URL. 

**Important:** The password contains special characters that need URL encoding:
- Password: `@Penske@#09871`
- URL encoded: `%40Penske@%2309871` (the `@` becomes `%40` and `#` becomes `%23`)

#### Option A: Set .env manually
Create or update `.env` in `customer-service/` with:
```
DATABASE_URL=postgresql+asyncpg://admin:%40Penske%40%2309871@localhost:5432/microservice
```
Note: When running with Docker Compose, use `postgres` as the host instead of `localhost`:
```
DATABASE_URL=postgresql+asyncpg://admin:%40Penske%40%2309871@postgres:5432/microservice
```

#### Option B: Use environment variable directly
```bash
export DATABASE_URL="postgresql+asyncpg://admin:%40Penske%40%2309871@localhost:5432/microservice"
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify Connection

Test the connection with:
```bash
cd customer-service
python3 << 'EOF'
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://admin:%40Penske%40%2309871@localhost:5432/microservice"

async def test():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        result = await conn.execute("SELECT 1")
        print("✅ Connection successful!")

asyncio.run(test())
EOF
```

### Step 4: Run the Application

```bash
cd customer-service
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application should now connect to PostgreSQL successfully!

### Step 5: Seed the Database (Optional)

To populate the database with sample customer data for testing:

```bash
cd customer-service
python3 seed_db.py
```

This will create 5 sample customers in the database. You can verify by accessing:
```bash
curl http://localhost:8000/customers
```

## URL Encoding Reference

If your password contains special characters, they need to be URL encoded:

| Character | Encoded | Character | Encoded |
|-----------|---------|-----------|---------|
| `#`       | `%23`   | `@`       | `%40`   |
| `:`       | `%3A`   | `/`       | `%2F`   |
| `?`       | `%3F`   | `&`       | `%26`   |
| `%`       | `%25`   | ` ` (space) | `%20` |

## Connection String Format

```
postgresql+asyncpg://[username]:[password]@[host]:[port]/[database]
```

Where:
- `username`: `admin`
- `password`: `%40Penske@%2309871` (URL encoded - note the first `@` becomes `%40`)
- `host`: `localhost` (or `postgres` if using docker-compose)
- `port`: `5432`
- `database`: `microservice`
