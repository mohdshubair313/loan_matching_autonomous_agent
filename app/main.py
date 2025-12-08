from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import traceback
from .database import engine, get_session, Base
from .routers import uploads  # upload.py file
from .crud import get_recent_users

app = FastAPI(title="Loan Eligibility Engine Backend")

app.include_router(uploads.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created!")
    except Exception as e:
        print(f"Startup DB skip: {e}")  # Fail silent, manual tables OK

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r", encoding='utf-8') as f:
        return f.read()

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_session)):
    try:
        users = await get_recent_users(db)
        return {"users": [u.__dict__ for u in users]}
    except Exception as e:
        return {"error": str(e), "users": []}
