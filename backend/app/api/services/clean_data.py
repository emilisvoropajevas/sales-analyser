import pandas as pd
from io import BytesIO

required_columns = ['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']

def clean_and_format_data(csv_file):
    try:
        uploaded_file_as_dataframe = pd.read_csv(BytesIO(csv_file))
    except Exception:
        raise ValueError("Could not parse CSV file")
    if uploaded_file_as_dataframe.empty:
        raise ValueError("CSV File is empty")
    
    missing_columns = set(required_columns) - set(uploaded_file_as_dataframe.columns)
    if missing_columns:
        raise ValueError(f"Column {missing_columns} missing from Dataframe")

    uploaded_file_as_dataframe['Order Date'] = (pd.to_datetime(uploaded_file_as_dataframe['Order Date'], errors = 'coerce')).dt.normalize()

    if uploaded_file_as_dataframe['Order Date'].isnull().sum() / len(uploaded_file_as_dataframe['Order Date']) > 0.1:
        raise ValueError("Too many null date rows")
    else:
        uploaded_file_as_dataframe['Order Date'].dropna()
    
    report_dataframe = uploaded_file_as_dataframe[['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']].copy()
    
     # - Business Logic
    report_dataframe = report_dataframe[report_dataframe['Product SKU'].str.contains("-f", na = False)]

    # - Order in ascending order
    report_dataframe = report_dataframe.sort_values(by = 'Order Date', ascending= True).reset_index(drop = True)

    report_dataframe['Model Range'] = report_dataframe['Product SKU'].str.rsplit("/", n=1).str[0]
    
    start_date = report_dataframe['Order Date'].min()
    end_date = report_dataframe['Order Date'].max()

    return start_date, end_date, report_dataframe