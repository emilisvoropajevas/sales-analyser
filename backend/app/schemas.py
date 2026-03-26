from pydantic import BaseModel, AfterValidator
from datetime import datetime
from typing import Annotated

#Validate input type "" to make sure it's not accepted for save endpoint
def is_empty(value: str) -> str:
    if not value.strip():
        raise ValueError("Name can't be blank")
    return value.strip()

class ReportRow(BaseModel):
    order_date: datetime
    order_id: int
    product_sku: str
    product_name: str
    quantity_ordered: float
    price: float
    model_range: str

class SaveUpload(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)]
    start_date: datetime
    end_date: datetime
    data: list[ReportRow] = []

class ReportsHistory(BaseModel):
    id: int
    name: str
    created_at: datetime
    date_range_start: datetime
    date_range_end: datetime

class UpdateReport(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)]

