from pydantic import BaseModel
from datetime import datetime

#['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']

class ReportRow(BaseModel):
    order_date: datetime
    order_id: int
    product_sku: str
    product_name: str
    quantity_ordered: float
    price: float
    model_range: str



class SaveUpload(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    data: list[ReportRow] = []
