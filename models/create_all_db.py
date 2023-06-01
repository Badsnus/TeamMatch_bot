from sqlalchemy.ext.asyncio import AsyncEngine

from models.base_model import Base


async def create_all_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
