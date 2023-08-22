from src.config import db_user, db_host, db_name, db_password
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = f"mysql+aiomysql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Session = async_session_maker(bind=engine)


def get_session():
    session = Session
    try:
        yield session
    finally:
        session.close()


class Base(DeclarativeBase):
    pass




