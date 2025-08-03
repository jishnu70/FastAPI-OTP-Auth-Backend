# main.py

from fastapi import FastAPI
import uvicorn
from app.database import engine, Base
from contextlib import asynccontextmanager
from routes.authRoutes import authRoute
import logging

logger = logging.getLogger(__name__)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database created successfully")
    except Exception as e:
        logger.error(f"Error initializing DB: {str(e)}")
        raise

async def close_db():
    try:
        await engine.dispose()
        print("Database disposed successfully")
    except Exception as e:
        logger.error(f"Error closing DB: {str(e)}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)
app.include_router(authRoute)

@app.get("/")
def root():
    return {"message": "backend is online"}

def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()
