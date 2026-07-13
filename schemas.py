from pydantic import BaseModel

class StudentsCreate(BaseModel):
    name: str
    age: int
    city: str 

class Student(StudentsCreate):
    id: int
    
    class Config:
        from_attributes = True