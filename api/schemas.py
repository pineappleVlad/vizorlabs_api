from datetime import datetime
from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    full_name: str
    login: str
    password: str
    email: str
    subdivision_id: int

class SubdivisionSchema(BaseModel):
    name: str
    supervisor_id: int

class BusinessTripScheduleSchema(BaseModel):
    start_date: datetime
    end_date: datetime
    employee_id: int

class VacationScheduleSchema(BaseModel):
    start_date: datetime
    end_date: datetime
    employee_id: int
