import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, text
from app.core.config import settings

postgres_url = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

print("🔧 Connecting to:", postgres_url)

try:
    engine = create_engine(postgres_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ PostgreSQL connected successfully!")
        print("   Version:", result.scalar())
except Exception as e:
    print("❌ Connection failed:")
    print(e)
