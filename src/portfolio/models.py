from src.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
#from src.models import User


class DicProgramLang(Base):
    __tablename__ = "dic_program_lang"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)


class PortfolioDatabase(Base):
    __tablename__ = "portfolio_database"

    id = Column(Integer, autoincrement=True, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), nullable=False)
    database_id = Column(Integer, ForeignKey("dic_database.id"), nullable=False)


class PortfolioProgramLang(Base):
    __tablename__ = "portfolio_program_lang"

    id = Column(Integer, autoincrement=True, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), nullable=False)
    program_lang_id = Column(Integer, ForeignKey("dic_program_lang.id"), nullable=False)


class PortfolioKnowledgeField(Base):
    __tablename__ = "portfolio_knowledge_field"

    id = Column(Integer, autoincrement=True, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), nullable=False)
    knowledge_field_id = Column(Integer, ForeignKey("dic_knowledge_field.id"), nullable=False)


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date_create = Column(DateTime, nullable=False)
    work_experience = Column(Integer, default=0)
    knowledge_field = Column(Integer, default=0)
    github_link = Column(String)
    linkedin_link = Column(String)
    hh_link = Column(String)
    work_schedule = Column(Integer, default=0)




