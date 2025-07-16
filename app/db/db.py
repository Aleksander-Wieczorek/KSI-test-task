import asyncpg
import os
import asyncio
import logging
from typing import Optional
from asyncpg.exceptions import PostgresError

logging.basicConfig(level=logging.INFO)

class DatabaseConnection:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self, retries=3, delay=2):
        """Initialize connection pool with retries"""
        database_url = os.getenv("DATABASE_URL", "postgres://postgres:postgres@fastapi-template-db:5432/todo")
        for attempt in range(retries):
            try:
                self.pool = await asyncpg.create_pool(
                    database_url,
                    min_size=2,
                    max_size=10,
                    timeout=10  # 10 sekund timeout na połączenie
                )
                logging.info("Database connection established")
                return
            except PostgresError as e:
                logging.warning(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
        raise RuntimeError("Failed to connect to database after multiple attempts")
    
    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logging.info("Database connection closed")
    
    async def get_connection(self):
        """Get a connection from the pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized. Call connect() first.")
        return await self.pool.acquire()

# Global database instance
db = DatabaseConnection()