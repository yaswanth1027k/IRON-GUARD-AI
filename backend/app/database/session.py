from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

# Create the async engine
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    echo=False,  # Set to True if you want to see the raw SQL queries in the console
    future=True
)

# Create a session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to inject the database session into your FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session