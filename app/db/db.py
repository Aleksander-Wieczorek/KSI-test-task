import asyncpg
import os
import asyncio
import logging
from typing import Optional, List, Dict
from asyncpg.exceptions import PostgresError

logging.basicConfig(level=logging.INFO)

class DatabaseConnection:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    async def fetch_all(self, query: str):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)

    async def fetch(self, query: str, *args) -> List[Dict]:
        """Fetch rows with parameters"""
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, *args)
            return [dict(row) for row in rows]
    async def connect(self, retries=3, delay=2):
        """Initialize connection pool with retries"""
        database_url = os.getenv("DATABASE_URL", "postgres://postgres:postgres@db:5432/todo")
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
async def get_tasks():
    return await db.fetch_all("SELECT * FROM tasks")
async def add_task(note):
    query = """
            INSERT INTO tasks (note)
            VALUES ($1)
            """
    try:
        result = await db.fetch(query, note)
        return dict(result[0]) if result else None
    except Exception as e:
        logging.error(f"Błąd przy dodawaniu zadania: {e}")
        raise
async def delete_task(id):
    query = """
            DELETE FROM tasks 
            WHERE id = $1
            RETURNING id
        """
    try:
        await db.fetch(query, id)
        return {"status": "success", "deleted_id": id}
    except Exception as e:
        logging.error(f"Błąd przy usuwaniu zadania: {e}")
        raise