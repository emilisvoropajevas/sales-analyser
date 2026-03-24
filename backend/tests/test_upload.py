from fastapi.testclient import TestClient
from app.main import app
import pandas as pd

required_columns = ['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']

test_dataframe = pd.DataFrame({
    'Order Date': ['2024-01-01', '2024-02-02'],
    'Order ID': ['000321321', '000432432'],
    'Product SKU': ['ABC-f/1', 'DEF-f/2'],
    'Product Name': ['Product A', 'Product B'],
    'Qty Ordered': [2, 3],
    'Price': [10.99, 5.99]
})

empty_test_dataframe = pd.DataFrame({
    'Order Date': [],
    'Order ID': [],
    'Product SKU': [],
    'Product Name': [],
    'Qty Ordered': [],
    'Price': []
})

many_null_dates_dataframe = pd.DataFrame({
    'Order Date': ['2024-01-01', '2024-02-02', '0000-00-00','0000-00-00'],
    'Order ID': ['000321321', '000432432','000133233', '000123432'],
    'Product SKU': ['ABC-f/1', 'DEF-f/2','CBD-f/2','BCD-f/4'],
    'Product Name': ['Product A', 'Product B','Product C', 'Product D'],
    'Qty Ordered': [2, 3, 4, 5],
    'Price': [10.99, 5.99, 6.99, 7.99]
})

missing_columns_dataframe = pd.DataFrame({
    'Order Date': ['2024-01-01', '2024-02-02'],
    'Order ID': ['000321321', '000432432'],
    'Product SKU': ['ABC-f/1', 'DEF-f/2'],
    'Product Name': ['Product A', 'Product B'],
})

test_csv = test_dataframe.to_csv(index=False).encode()
test_empty_csv = empty_test_dataframe.to_csv(index=False).encode()
many_null_date_csv = many_null_dates_dataframe.to_csv(index=False).encode()
missing_columns_csv = missing_columns_dataframe.to_csv(index=False).encode()

client = TestClient(app)

def test_upload_wrong_file_type():
    response = client.post("/reports/upload", files={"file" : ("test_file.txt", b"This is test file", "text/plain")})
    assert response.status_code == 415
    assert response.json() == {"detail" : "File must be CSV"}

def test_upload_file_too_large():
    response = client.post("/reports/upload", files={"file" : ("file_over_5Mb.txt", b"x"*(6*1024*1024), "text/csv")})
    assert response.status_code == 413
    assert response.json() == {"detail" : "Filesize too large, must be below 5.0 Mb"}

def test_upload_success():
    response = client.post("/reports/upload", files={"file" : ("test_csv.csv", test_csv, "text/csv")})
    assert response.status_code == 200

def test_upload_empty_csv():
    response = client.post("/reports/upload", files={"file": ("empty_test_dataframe.csv", empty_test_dataframe, "text/csv")})
    assert response.json() == {"detail": "There was an error parsing the body"}

def test_upload_many_null_dates():
    response = client.post("/reports/upload", files={"file": ("many_null_date_csv.csv", many_null_date_csv, "text/csv")})
    assert response.json() == {"detail": "Too many null date rows"}

def test_upload_missing_columns():
    response = client.post("/reports/upload", files={"file": ("missing_columns_csv.csv", missing_columns_csv, "text/csv")})
    assert response.json() == {"detail": "Column {'Qty Ordered', 'Price'} missing from Dataframe"}