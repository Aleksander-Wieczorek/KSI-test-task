from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.router.health import router as health_router
from app.router.todos import router as todos_router
from app.db.db import db
import logging
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            await db.connect()
            logging.info("Database connection established")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logging.warning(f"Attempt {attempt+1} failed: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, 30)
            else:
                logging.error(f"Final connection failed: {e}")
                raise
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(health_router)
app.include_router(todos_router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})