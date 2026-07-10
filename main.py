from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional #optional fields

app = FastAPI()

students = []

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Student(BaseModel): #pydantic model
    id: int #type hints
    name: str = Field(min_length=3, max_length=20)
    age: int = Field(gt=0, lt=100)
    email: EmailStr
    phone: Optional[str] = None
    address: Address

@app.post("/students")
def add_student(student: Student):
    students.append(student.dict())
    print(students)
    return {
        "message": "Student added successfuly!"
    }
    
@app.get("/students")
def get_students():
    return students

@app.put("/students/{id}")
def update_student(id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student["id"] == id:
            new_student = updated_student.model_dump()
            new_student["id"] = id
            students[index] = new_student
            
            return {
                "message": "Student updated successfully!"
            }
    
    return {
        "message": "Student not found"
    }

@app.delete("/students/{id}")
def delete_student(id: int):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            
            return {
                "message": "Student Deleted"
            }
    
    return {
        "message": "Student not found"
    }










# def home():
#     return {
#         "message": "Welcome to FastAPI"
#     }

# @app.get("/about")
# def about():
#     return {
#         "message": "About Page"
#     }
# #JSON -> Javascript Object Notation

# @app.get("/hello")
# def hello():
#     return {
#         "student": {
#             "name": "Hassan",
#             "age": 23,
#             "city": "Lahore"
#         }
#     }
    
# #Path parameters
# @app.get("/products/{product_id}")

# def get_product(product_id: int):
#     return {
#         "product_id": product_id
#     }

# #Multiple path parameters
# @app.get("/products/{product_id}/reviews/{review_id}")
# def get_product(product_id: int, review_id: int):
#     return {
#         "product_id": product_id,
#         "review_id": review_id
#     }
    
# #Query Parameter
# # @app.get("/students")
# # def students(city:str):
# #     return {
# #         "city": city
# #     }
    
# #Multiple Query Parameter
# @app.get("/students")
# def get_students(city:str, age:int):
    
    # return {
    #     "city": city,
    #     "age": age
    # }