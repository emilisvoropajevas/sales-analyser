from fastapi import APIRouter, HTTPException
import json

from app.core.database import SessionDep
from app.models import Reports
from app.schemas import SaveUpload

"""
User is returned a cleaned dataframe and is asked to enter name and save report.
"""
router = APIRouter()

@router.post("/reports/save")
async def save_upload(upload_report: SaveUpload, session : SessionDep) -> Reports:
    #Since SaveUpload stores a list of object, need to serialise and dump each to convert to json to store as string
    upload_data_dict = []
    for row in upload_report.data:
        upload_data_dict.append(row.model_dump(mode="json"))

    upload_data_string = json.dumps(upload_data_dict)
    #Map Save upload -> Reports 
    new_report = Reports(
        name = upload_report.name,
        date_range_start = upload_report.start_date,
        date_range_end = upload_report.end_date,
        data = upload_data_string
    )
    session.add(new_report)
    session.commit()
    session.refresh(new_report)
    return new_report
