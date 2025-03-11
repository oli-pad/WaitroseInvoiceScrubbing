import pyodbc
import pandas as pd

def InsertIntoScrubbedStg(
    Salitix_client_number : str = "NULL"
      ,Salitix_customer_number : str = "WAI01"
      ,SAL_Invoice_Type : str = "NULL"
      ,Unit_Funding_Type : str = "NULL"
      ,Reference_Number : str = "NULL"
      ,Line_Description : str = "NULL"
      ,Deal_Type : str = "NULL"
      ,Invoice_No : str = "NULL"
      ,Invoice_Date : str = "NULL"
      ,Promotion_No : str = "NULL"
      ,Product_No : str = "NULL"
      ,Start_Date : str = "NULL"
      ,End_Date : str = "NULL"
      ,Quantity : str = "NULL"
      ,Unit_Price : str = "NULL"
      ,Net_Amount : str = "NULL"
      ,VAT_Rate : str = "NULL"
      ,Gross_Amount : str = "NULL"
      ,Store_Format : str = "NULL"
      ,Invoice_Description : str = "NULL"
      ,Acquisition_Ind : str = "Automatic"
      ,HDR_Invoice_Number : str = "NULL"
):
    
    # Connect to database
    conn = pyodbc.connect('DRIVER=SQL Server;SERVER=UKSALSQL02;DATABASE=Salitix_Scrubbed_Data_Staging;Trusted_Connection=Yes;UID=SALITIX\SQLSalitixAuditorUsers')
    
    # Create cursor
    cursor = conn.cursor()

    # Data to insert
    SQL_String = "INSERT INTO [Salitix_Scrubbed_Data_Staging].[dbo].[Scrubbed_Customer_Charges_Stg] " + \
    "([Salitix_client_number],[Salitix_customer_number],[SAL_Invoice_Type],[Unit_Funding_Type],[Reference_Number] " + \
    ",[Line_Description],[Deal_Type],[Invoice_No],[Invoice_Date],[Promotion_No],[Product_No],[Start_Date],[End_Date] " + \
    ",[Quantity],[Unit_Price],[Net_Amount],[VAT_Rate],[Gross_Amount],[Store_Format],[Invoice_Description],[Acquisition_Ind] " + \
    ",[HDR_Invoice_Number])" + \
    " VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})"

    def format_value(value):
        return "NULL" if value == "NULL" or value is None else f"'{value}'"

    formatted_values = [
        format_value(Salitix_client_number),
        format_value(Salitix_customer_number),
        format_value(SAL_Invoice_Type),
        format_value(Unit_Funding_Type),
        format_value(Reference_Number),
        format_value(Line_Description),
        format_value(Deal_Type),
        format_value(Invoice_No),
        format_value(Invoice_Date),
        format_value(Promotion_No),
        format_value(Product_No),
        format_value(Start_Date),
        format_value(End_Date),
        format_value(Quantity),
        format_value(Unit_Price),
        format_value(Net_Amount),
        format_value(VAT_Rate),
        format_value(Gross_Amount),
        format_value(Store_Format),
        format_value(Invoice_Description),
        format_value(Acquisition_Ind),
        format_value(HDR_Invoice_Number)
    ]

    # print(SQL_String.format(*formatted_values))

    cursor.execute(SQL_String.format(*formatted_values))
    
    # Commit changes
    conn.commit()
        
    # Close connection
    conn.close()