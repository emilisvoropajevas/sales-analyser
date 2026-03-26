from fastapi import APIRouter

from typing import Annotated
from sqlmodel import select
from app.core.database import SessionDep
from app.schemas import ReportsHistory
from app.models import Reports

router = APIRouter()

@router.get("/reports/", response_model= list[ReportsHistory])
async def get_reports(session: SessionDep) -> list[ReportsHistory]:
    reports_history = session.exec(select(Reports)).all()
    return reports_history


#Endpoint for getting recent reports 


#Allow user to open, rename and delete