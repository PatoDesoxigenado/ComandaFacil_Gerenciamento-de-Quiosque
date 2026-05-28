from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.settings import get_settings

# Importa a biblioteca do MongoDB para o Python conseguir conversar 
from pymongo import MongoClient

settings = get_settings()

# --- CONEXÃO DO POSTGRESQL (Banco de Escrita - Já existia) ---
engine = create_async_engine(settings.DATABASE_URL, echo=settings.APP_DEBUG)

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass


# --- CONEXÃO DO MONGODB (Banco de Leitura - Adicionado AGORA) ---
#  usa a variável MONGO_URL que configurou no  .env
mongo_client = MongoClient(settings.MONGO_URL)

# Cria o acesso direto ao banco de dados de relatórios e dashboards
mongo_db = mongo_client.get_default_database()