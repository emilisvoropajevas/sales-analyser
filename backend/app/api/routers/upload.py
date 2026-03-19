from fastapi import UploadFile, APIRouter, HTTPException
from app.api.services.clean_data import clean_and_format_data

router = APIRouter()
"""
Upload Endpoint - This is where the user clicks a button called new (And drags and drops the csv)

"""

MAX_FILE_SIZE = 5 * 1024 * 1024

@router.post("/reports/upload")
async def clean_upload(file : UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"Filesize too large, must be below {MAX_FILE_SIZE/(1024*1024)} Mb")
    if file.content_type != "text/csv":
        raise HTTPException(status_code=415, detail="File must be CSV")
    #Return cleaned dataframe file as a json to frontend
    contents = await file.read()
    try:
        start_date, end_date, report_dataframe = clean_and_format_data(contents)
    except ValueError as error_value:
        raise HTTPException(status_code=422, detail=str(error_value))
    
    #Rename columns to match ReportRow schema
    report_dataframe = report_dataframe.rename(columns={
        "Order Date": "order_date",
        "Order ID": "order_id",
        "Product SKU": "product_sku",
        "Product Name": "product_name",
        "Qty Ordered": "quantity_ordered",
        "Price": "price",
        "Model Range": "model_range"

    })

    return {
        "start_date": start_date,
        "end_date": end_date,
        "report_data": report_dataframe.to_dict(orient="records")
    }
