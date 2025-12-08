from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def create_users(session: AsyncSession, users_data: list[schemas.UserCreate]):
    """Bulk insert users"""
    db_users = [models.User(**user.dict()) for user in users_data]
    session.add_all(db_users)
    await session.commit()
    await session.refresh_all(db_users)
    return db_users

async def get_recent_users(session: AsyncSession, limit: int = 10):
    stmt = select(models.User).order_by(models.User.created_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

# Later for matches, etc.
