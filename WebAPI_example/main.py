from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import date

app = FastAPI()
DATABASE_URL = "sqlite:///./employees.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EmployeeDB(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    hire_date = Column(Date, nullable=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Employee(BaseModel):
    name: str
    department: str
    salary: int
    hire_date: date

class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    salary: int
    hire_date: date
    
    class Config:
        from_attributes = True

@app.get("/employees/{employee_id}")
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "id": employee.id,
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary,
        "hire_date": employee.hire_date
    }

@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(emp: Employee, db: Session = Depends(get_db)):
    db_employee = EmployeeDB(
        name=emp.name,
        department=emp.department,
        salary=emp.salary,
        hire_date=emp.hire_date
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return {"id": db_employee.id, "employee": emp}

@app.put("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_employee(employee_id: int, emp: Employee, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee.name = emp.name
    db_employee.department = emp.department
    db_employee.salary = emp.salary
    db_employee.hire_date = emp.hire_date
    
    db.commit()
    return

@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return

@app.get("/secure-info")
def get_secure_info(token: Optional[str] = None):
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Access granted"}

@app.get("/admin")
def get_admin(is_admin: bool = False):
    if not is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "Welcome, admin"}

Base.metadata.create_all(bind=engine)