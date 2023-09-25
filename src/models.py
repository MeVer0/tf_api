from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Double, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_author = Column(Boolean, default=False)


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    logo = Column(String)
    author_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Double, nullable=False)


class CourseModule(Base):
    __tablename__ = "course_module"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False,)
    name = Column(String, nullable=False)

    f_key_course = relationship('Course')


class CourseStep(Base):
    __tablename__ = "course_step"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, nullable=False)
    module_id = Column(Integer, ForeignKey("course_module.id"), nullable=False)
    video = Column(String, nullable=False)
    image = Column(String, default=True)
    text = Column(String, default=True)

    f_key_module = relationship('CourseModule')


class UserCourse(Base):
    __tablename__ = "user_course"

    user_id = Column(Integer)
    course_id = Column(Integer, primary_key=True)
    type_id = Column(Integer, primary_key=True)

    __table_args__ = (UniqueConstraint('user_id', 'course_id', name='user_id_course_id'), )
