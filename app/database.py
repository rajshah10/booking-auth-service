
# SQL Alchemy (ORM)

# Instead of writing raw SQL like SELECT * FROM users WHERE id = 1, SQLAlchemy lets you interact with your database using Python classes and objects
# If you start building your application using MySQL, but later decide you need to switch to PostgreSQL or SQLite (e.g., for local testing), you would normally have to rewrite many of your raw SQL queries because different databases have slightly different syntax.

# You write your code once using SQLAlchemy, and it works with MySQL, PostgreSQL, SQLite, MSSQL, Oracle, and many other databases without you having to rewrite your queries.

# Prevents SQL injection Attack
# Connection Pooling - opening a new connection to a database every time a user makes a request is slow and expensive. SQLAlchemy’s engine automatically manages a "pool" of active database connections. 


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()    

DB_HOST= os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_NAME= os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL,pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base=declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

