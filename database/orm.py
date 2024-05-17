from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, Any
from datetime import datetime

from .db_connection import get_session
from .models import Employee, Subdivision, VacationSchedule, BusinessTripSchedule


class CRUDOperations: # Базовый класс для CRUD-операций
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def get(self, model: Type, id: int) -> Any:
        result = await self.db.execute(select(model).where(model.id == id))
        return result.scalars().first()
    async def create(self, obj: Any) -> Any:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: Any) -> Any:
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Any) -> Any:
        await self.db.delete(obj)
        await self.db.commit()


class EmployeeCRUD(CRUDOperations): # Класс для сотрудников
    async def create_employee(self, full_name: str, login: str, password: str, email: str, subdivision_id: int) -> Employee:
        employee = Employee(full_name=full_name, login=login, password=password, email=email, subdivision_id=subdivision_id)
        return await self.create(employee)

    async def update_employee(self, employee: Employee, **kwargs: dict) -> Employee:
        for key, value in kwargs.items():
            setattr(employee, key, value)
        return await self.update(employee)

    async def delete_employee(self, employee_id: int) -> bool:
        employee = self.get(Employee, employee_id)
        if employee:
            await self.db.delete(employee)
            return True
        else:
            return False

    async def get_employee(self, employee_id: int) -> Employee:
        return await self.get(Employee, employee_id)


class SubdivisionCRUD(CRUDOperations): # Класс для подразделений
    async def create_subdivision(self, name: str, supervisor_id: int) -> Subdivision:
        subdivision = Subdivision(name=name, supervisor_id=supervisor_id)
        return await self.create(subdivision)

    async def update_subdivision(self, subdivision: Subdivision, **kwargs: dict) -> Subdivision:
        for key, value in kwargs.items():
            setattr(subdivision, key, value)
        return await self.update(subdivision)

    async def delete_subdivision(self, subdivision_id: int) -> bool:
        subdivision = await self.get(Subdivision, subdivision_id)
        if subdivision:
            await self.db.delete(subdivision)
            return True
        else:
            return False

    async def get_subdivision(self, subdivision_id: int) -> Subdivision:
        return await self.get(Subdivision, subdivision_id)


class BusinessTripCRUD(CRUDOperations): # Класс для командировок
    async def create_business_trip(self, start_date: datetime, end_date: datetime, employee_id: int) -> BusinessTripSchedule:
        business_trip = BusinessTripSchedule(start_date=start_date, end_date=end_date, employee_id=employee_id)
        return await self.create(business_trip)

    async def update_business_trip(self, business_trip: BusinessTripSchedule, **kwargs: dict) -> BusinessTripSchedule:
        for key, value in kwargs.items():
            setattr(business_trip, key, value)
        return await self.update(business_trip)

    async def delete_business_trip(self, business_trip_id: int) -> bool:
        business_trip = await self.get(BusinessTripSchedule, business_trip_id)
        if business_trip:
            await self.db.delete(business_trip)
            return True
        else:
            return False

    async def get_business_trip(self, business_trip_id: int) -> BusinessTripSchedule:
        return await self.get(BusinessTripSchedule, business_trip_id)


class VacationCRUD(CRUDOperations): # Класс для отпусков
    async def create_vacation(self, start_date: datetime, end_date: datetime, employee_id: int) -> VacationSchedule:
        vacation = VacationSchedule(start_date=start_date, end_date=end_date, employee_id=employee_id)
        return await self.create(vacation)

    async def update_vacation(self, vacation: VacationSchedule, **kwargs: dict) -> VacationSchedule:
        for key, value in kwargs.items():
            setattr(vacation, key, value)
        return await self.update(vacation)

    async def delete_vacation(self, vacation_id: int) -> bool:
        vacation = await self.get(VacationSchedule, vacation_id)
        if vacation:
            await self.db.delete(vacation)
            return True
        else:
            return False

    async def get_vacation(self, vacation_id: int) -> VacationSchedule:
        return await self.get(VacationSchedule, vacation_id)


employee_crud = EmployeeCRUD(db_session=Depends(get_session))
subdivision_crud = SubdivisionCRUD(db_session=Depends(get_session))
business_trip_crud = BusinessTripCRUD(db_session=Depends(get_session))
vacation_schedule_crud = VacationCRUD(db_session=Depends(get_session))