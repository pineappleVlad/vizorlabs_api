from sqlalchemy import Column, String, Integer, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from .db_connection import Base

class Employee(Base): # Модель для сотрудников
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String)
    login = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)

    subdivision_id = Column(Integer, ForeignKey('subdivisions.id'))
    subdivision = relationship("Subdivision", back_populates="employees", foreign_keys=[subdivision_id])

    business_trip_schedule = relationship("BusinessTripSchedule", back_populates="employee")
    vacation_schedule = relationship("VacationSchedule", back_populates="employee")

class Subdivision(Base): # Модель для подразделений
    __tablename__ = "subdivisions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    supervisor_id = Column(Integer, ForeignKey('employees.id'))
    supervisor = relationship("Employee", back_populates="subdivision", uselist=False, foreign_keys=[supervisor_id], remote_side=[Employee.id])
    employees = relationship("Employee", back_populates="subdivision", foreign_keys=[Employee.subdivision_id])

class BusinessTripSchedule(Base): # Модель для командировок
    __tablename__ = "business_trip_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_trip = Column(Date)
    end_trip = Column(Date)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="business_trip_schedule")


class VacationSchedule(Base): # Модель для отпусков
    __tablename__ = "vacation_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_trip = Column(Date)
    end_trip = Column(Date)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="vacation_schedule")

