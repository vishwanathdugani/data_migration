from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # Defines the location of the SQLite database

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Necessary for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Base class for your models to inherit from
