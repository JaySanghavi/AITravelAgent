from sqlalchemy.ext.asyncio import create_async_engine
from db.models import Base

engine = create_async_engine("mysql+aiomysql://user:pass@localhost/flyhigh")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
