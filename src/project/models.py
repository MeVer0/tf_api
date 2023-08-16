from src.database import Base


from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date_create = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    application_field = Column(Integer, default=0)
    is_commercial = Column(Boolean, nullable=False)
    development_stage = Column(Integer, default=0)


class ProjectProgramLang(Base):
    __tablename__ = "project_program_lang"

    id = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    program_lang_id = Column(Integer, ForeignKey("dic_program_lang.id"), nullable=False)
