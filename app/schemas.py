from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from decimal import Decimal

class UserCreate(BaseModel):
    user_id: str
    email: EmailStr
    monthly_income: float
    credit_score: int
    employment_status: str
    age: int

    @field_validator('credit_score')
    @classmethod
    def validate_score(cls, v):
        if not 300 <= v <= 900:
            raise ValueError('Credit score must be 300-900')
        return v

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if not 18 <= v <= 80:
            raise ValueError('Age must be 18-80')
        return v
