from fastapi.testclient import TestClient
from app.main import app
from app.api.routers import upload
from io import BytesIO
import pandas as pd

client = TestClient(app)

def test_upload_wrong_file_type():
    response = client.post("/upload", files={"file" : ("test_file.txt", b"This is test file", "text/plain")})
    assert response.status_code == 415
    assert response.json() == {"detail" : "File must be CSV"}

def test_upload_file_too_large():
    response = client.post("/upload", files={"file" : ("file_over_5Mb.txt", b"x"*(6*1024*1024), "text/csv")})
    assert response.status_code == 413
    assert response.json() == {"detail" : "Filesize too large, must be below 5.0 Mb"}

test_dataframe = pd.DataFrame({
    'Order Date': ['2024-01-01', '2024-02-02'],
    'Order ID': ['000321321', '432432'],
    'Product SKU': ['ABC-f/1', 'DEF-f/2'],
    'Product Name': ['Product A', 'Product B'],
    'Qty Ordered': [2, 3],
    'Price': [10.99, 5.99]
})

test_csv = test_dataframe.to_csv(index=False).encode()


def test_upload_success():
    response = client.post("/upload", files={"file" : ("test_csv.csv", test_csv, "text/csv")})
    assert response.status_code == 200