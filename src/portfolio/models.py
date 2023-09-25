from src.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.models import User


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date_create = Column(DateTime, nullable=False)
    work_experience = Column(Integer, default=0)
    github_link = Column(String)
    linkedin_link = Column(String)
    hh_link = Column(String)


class PortfolioTechnology(Base):
    __tablename__ = "portfolio_technology"

    id = Column(Integer, autoincrement=True, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), nullable=False)
    technology_id = Column(Integer, nullable=False)  # src.models модель DicCodeTechnology.id


class PortfolioKnowledgeField(Base):
    __tablename__ = "portfolio_knowledge_field"

    id = Column(Integer, autoincrement=True, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), nullable=False)
    knowledge_field_id = Column(Integer, ForeignKey("dic_knowledge_field.id"), nullable=False)






