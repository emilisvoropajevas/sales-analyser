from datetime import datetime
from sqlmodel import Field, SQLModel

class Reports(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    created_at : datetime = Field(default=datetime.now(tz=datetime.UTC))
    date_range_start : str
    date_range_end : str
    data : str
