from fastapi import Depends, FastAPI, HTTPException
from requests import Session
from database import engine, SessionLocal
from models import Base, Student
import schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students", response_model=list[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.post("/students", response_model=schemas.Student)
def add_student(student: schemas.StudentsCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name = student.name,
        age = student.age,
        city = student.city
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    return student

@app.put("/students/{id}", response_model=schemas.StudentsCreate)
def update_student(id: int, updated: schemas.StudentsCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    student.name = updated.name
    student.age = updated.age
    student.city = updated.city
    
    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()
    
    return {
        "message": "Student deleted successfully"
    }




# #ORM = object relational mapping

# from pydantic import BaseModel, Field, EmailStr
# from typing import Optional #optional fields



# students = []

# class Address(BaseModel):
#     street: str
#     city: str
#     country: str
#     postal_code: str

# class Student(BaseModel): #pydantic model
#     id: int #type hints
#     name: str = Field(min_length=3, max_length=20)
#     age: int = Field(gt=0, lt=100)
#     email: EmailStr
#     phone: Optional[str] = None
#     address: Address
#     password: str
    
# class StudentResponse(BaseModel):
#     id: int
#     name: str
#     email: EmailStr

# @app.post("/students")
# def add_student(student: Student):
#     students.append(student.dict())
#     print(students)
#     return {
#         "message": "Student added successfuly!"
#     }
    


# @app.put("/students/{id}")
# def update_student(id: int, updated_student: Student):
#     for index, student in enumerate(students):
#         if student["id"] == id:
#             new_student = updated_student.model_dump()
#             new_student["id"] = id
#             students[index] = new_student
            
#             return {
#                 "message": "Student updated successfully!"
#             }
    
#     return {
#         "message": "Student not found"
#     }

# @app.delete("/students/{id}")
# def delete_student(id: int):
#     for student in students:
#         if student["id"] == id:
#             students.remove(student)
            
#             return {
#                 "message": "Student Deleted"
#             }
    
#     return {
#         "message": "Student not found"
#     }










# # def home():
# #     return {
# #         "message": "Welcome to FastAPI"
# #     }

# # @app.get("/about")
# # def about():
# #     return {
# #         "message": "About Page"
# #     }
# # #JSON -> Javascript Object Notation

# # @app.get("/hello")
# # def hello():
# #     return {
# #         "student": {
# #             "name": "Hassan",
# #             "age": 23,
# #             "city": "Lahore"
# #         }
# #     }
    
# # #Path parameters
# # @app.get("/products/{product_id}")

# # def get_product(product_id: int):
# #     return {
# #         "product_id": product_id
# #     }

# # #Multiple path parameters
# # @app.get("/products/{product_id}/reviews/{review_id}")
# # def get_product(product_id: int, review_id: int):
# #     return {
# #         "product_id": product_id,
# #         "review_id": review_id
# #     }
    
# # #Query Parameter
# # # @app.get("/students")
# # # def students(city:str):
# # #     return {
# # #         "city": city
# # #     }
    
# # #Multiple Query Parameter
# # @app.get("/students")
# # def get_students(city:str, age:int):
    
#     # return {
#     #     "city": city,
#     #     "age": age
#     # }