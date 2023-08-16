from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase

from src.database import Base
from src.portfolio.models import Portfolio
from src.project.models import Project


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    portfolio = relationship("Portfolio")
    project = relationship("Project")


# Таблицы справочнки
class DicKnowledgeField(Base):
    __tablename__ = "dic_knowledge_field"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)


class DicWorkSchedule(Base):
    __tablename__ = "dic_work_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)


class DicDatabase(Base):
    __tablename__ = "dic_database"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)