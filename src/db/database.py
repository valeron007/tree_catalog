from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from decouple import config

SQLALCHEMY_DATABASE_URL: str = f"postgresql://{config('DATABASE_USER')}:{config('DATABASE_PASSWORD')}@173.10.1.3/{config('DATABASE_NAME')}"

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal: sessionmaker[Session] = sessionmaker(autoflush=False, bind=engine)
db: Session = SessionLocal()

Base = declarative_base()
