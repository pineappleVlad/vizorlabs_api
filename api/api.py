from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_connection import get_session
from database.orm import employee_crud, subdivision_crud, business_trip_crud, vacation_schedule_crud
from database.models import Employee, Subdivision, VacationSchedule, BusinessTripSchedule
from .schemas import *

app = FastAPI()

@app.post("/employee", response_model=EmployeeSchema)
async def create_employee(employee: EmployeeSchema):
    return await employee_crud.create_employee(**employee.dict())

