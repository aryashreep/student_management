from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import Student
from backend.database import get_db
from backend.models import Student as StudentModel

router = APIRouter()


@router.post("/students", status_code=201)
async def add_student(body: Student, db: AsyncSession = Depends(get_db)):
    """Add a new student"""
    # Check if student ID already exists
    result = await db.execute(select(StudentModel).where(StudentModel.id == body.id))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Student with this ID already exists")

    # Check if email already exists
    result = await db.execute(select(StudentModel).where(StudentModel.email == body.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Student with this email already exists")

    student = StudentModel(**body.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student.to_dict()


@router.get("/students")
async def get_students(db: AsyncSession = Depends(get_db)):
    """Get all students"""
    result = await db.execute(select(StudentModel).order_by(StudentModel.id))
    students = result.scalars().all()
    return [s.to_dict() for s in students]


@router.get("/students/{student_id}")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific student by ID"""
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.to_dict()


@router.put("/students/{student_id}")
async def update_student(student_id: int, body: Student, db: AsyncSession = Depends(get_db)):
    """Update a student"""
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if new email is already used by another student
    if body.email != student.email:
        result = await db.execute(select(StudentModel).where(StudentModel.email == body.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already in use")

    student.name = body.name
    student.age = body.age
    student.course = body.course
    student.email = body.email

    await db.commit()
    await db.refresh(student)

    return student.to_dict()


@router.delete("/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a student"""
    result = await db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()

    return {"message": "Student deleted successfully"}
