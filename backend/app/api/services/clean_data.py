import pandas as pd
from datetime import datetime
import io

#Cleaning function for uploaded data

def clean_and_format_data(csv_file):
    uploaded_file_as_dataframe = pd.read_csv(io.BytesIO(csv_file))
    uploaded_file_as_dataframe['Order Date'] = (pd.to_datetime(uploaded_file_as_dataframe['Order Date'], errors = 'coerce')).dt.normalize()

    # Select required fields - Order Date - Product SKU - Product Name - Price - Qty Ordered
    report_dataframe = uploaded_file_as_dataframe[['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']].copy()

    # - Remove matching threads and samples
    report_dataframe = report_dataframe[report_dataframe['Product SKU'].str.contains("-f", na = False)]

    # - Order in ascending order
    report_dataframe = report_dataframe.sort_values(by = 'Order Date', ascending= True).reset_index(drop = True)

    #Add in Model Column
    report_dataframe['Model Range'] = report_dataframe['Product SKU'].str.rsplit("/", n=1).str[0]
    
    return report_dataframe