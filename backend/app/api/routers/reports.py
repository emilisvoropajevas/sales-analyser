from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from typing import Annotated
from sqlmodel import select

from app.core.database import SessionDep
from app.schemas import ReportsHistory, UpdateReport
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

@router.put("/reports/{report_id}")
async def update_report(report_id: int, change_name: UpdateReport , session: SessionDep) -> Reports:
    report_to_update = session.get(Reports, report_id)
    if not report_to_update:
        raise HTTPException(status_code=404, detail="Report not found")
    report_to_update.name = change_name.name
    session.commit()
    session.refresh(report_to_update)
    return report_to_update
