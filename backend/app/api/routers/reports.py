from fastapi import APIRouter, HTTPException

from typing import Annotated
from sqlmodel import select
from app.core.database import SessionDep
from app.schemas import ReportsHistory
from app.models import Reports

router = APIRouter()

#Endpoint for getting recent reports 
@router.get("/reports/", response_model= list[ReportsHistory])
async def get_reports(session: SessionDep) -> list[ReportsHistory]:
    reports_history = session.exec(select(Reports)).all()
    return reports_history

#Allow user to open, rename and delete
@router.get("/reports/{report_id}")
async def open_report(report_id: int, session: SessionDep) -> Reports:
    report = session.get(Reports, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

