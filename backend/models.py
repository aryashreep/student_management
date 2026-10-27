from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import validates
from backend.database import Base
from datetime import datetime


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    course = Column(String(100), nullable=False, index=True)
    email = Column(String(120), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("name must not be empty or whitespace-only")
        return value

    @validates("age")
    def validate_age(self, key, value):
        if value <= 17:
            raise ValueError("age must be greater than 17")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "email": self.email,
        }
