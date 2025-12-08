from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)  # From CSV
    email = Column(String, unique=True, index=True)
    monthly_income = Column(Float)
    credit_score = Column(Integer)
    employment_status = Column(String)
    age = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LoanProduct(Base):
    __tablename__ = "loan_products"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    interest_rate = Column(Float)
    min_monthly_income = Column(Float)
    min_credit_score = Column(Integer)
    min_age = Column(Integer)
    max_age = Column(Integer, nullable=True)
    eligibility_criteria = Column(String)  # JSON/text summary
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    loan_product_id = Column(Integer, ForeignKey("loan_products.id"))
    match_score = Column(Float)  # 0-1 from logic/LLM
    created_at = Column(DateTime(timezone=True), server_default=func.now())
