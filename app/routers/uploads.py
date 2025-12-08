from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from io import BytesIO
import tempfile
from pathlib import Path
from ..database import get_session
from ..schemas import UserCreate
from ..crud import create_users

router = APIRouter(prefix="/api", tags=["upload"])

def parse_csv_background(csv_path: str):
    """Background task: Read CSV, validate, insert"""
    # Note: Render disk ephemeral, but temp file for parse
    df = pd.read_csv(csv_path)
    required_cols = ['user_id', 'email', 'monthly_income', 'credit_score', 'employment_status', 'age']
    if not all(col in df.columns for col in required_cols):
        raise ValueError("Missing CSV columns")
    
    users_data = []
    for _, row in df.iterrows():
        try:
            user = UserCreate(
                user_id=str(row['user_id']),
                email=row['email'],
                monthly_income=float(row['monthly_income']),
                credit_score=int(row['credit_score']),
                employment_status=str(row['employment_status']),
                age=int(row['age'])
            )
            users_data.append(user)
        except Exception as e:
            print(f"Row skip: {e}")
    
    # Here trigger n8n webhook later
    print(f"Processed {len(users_data)} users")  # In prod, call webhook

@router.post("/upload-csv/")
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files")
    
    # Temp store (Render /tmp)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    background_tasks.add_task(parse_csv_background, tmp_path)  # Async parse after response
    return {"message": "CSV uploaded & processing started! Check /users"}
