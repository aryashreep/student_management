"""
Seed script to generate 100 sample students and insert into PostgreSQL
Run with: python -m backend.seed
"""
import asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import engine, AsyncSessionLocal, init_db
from backend.models import Student

fake = Faker()
COURSES = ["Computer Science", "Data Science", "Business", "Engineering", "Psychology",
           "Mathematics", "Physics", "Chemistry", "Biology", "Economics"]


async def seed_students():
    """Generate and insert 100 sample students"""
    # Initialize database tables
    await init_db()

    async with AsyncSessionLocal() as session:
        # Check if students already exist
        from sqlalchemy import text
        result = await session.execute(text("SELECT COUNT(*) FROM students"))
        count = result.scalar()

        if count > 0:
            print(f"Database already has {count} students. Skipping seed.")
            return

        students = []
        emails = set()

        for i in range(1, 101):
            # Generate unique email
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.add(email)

            student = Student(
                id=i,
                name=fake.name(),
                age=fake.random_int(min=18, max=35),
                course=fake.random_element(COURSES),
                email=email,
            )
            students.append(student)

        session.add_all(students)
        await session.commit()
        print(f"✅ Successfully seeded {len(students)} students!")


async def main():
    try:
        await seed_students()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
