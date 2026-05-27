from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app=FastAPI()


students = {
    1: {
        "name": "John",
        "age": 17,
        "year": "12th"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class updateStudent(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    year: Optional[str]=None


@app.get('/')

def index():
    return {'name':"First Data"}

@app.get('/get-students/{student_id}')
def get_student(student_id: int = Path(..., description="The ID of the student you want to view")):
    return students[student_id]



@app.get('/get-by-name/{student_id}')
def get_student(*,student_id:int ,name:Optional[str]=None, test: int):
    for i in students:
        if students[i]['name']==name and students[i]['age']==test:
            return students[i]
    return {"Data":"not found"}



@app.post('/create-student/{student_id}')
def create_student(student_id:int, student: Student):
    if student_id in students:
        return {"Error": "Student Exists"}
    students[student_id]=student.dict()
    return students[student_id]

@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: updateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name is not None:
        students[student_id]['name'] = student.name
    if student.age is not None:
        students[student_id]['age'] = student.age
    if student.year is not None:
        students[student_id]['year'] = student.year
    return students[student_id]

@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error":"Student does not exists"}
    del students[student_id]
    return {"Success":"Student was succesfully removed"}