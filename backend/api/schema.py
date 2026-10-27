from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator


class Student(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=1)]
    age: Annotated[int, Field(gt=17)]
    course: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def name_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty or whitespace-only")
        return v
