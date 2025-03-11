from group.waitroseIncoiceDetail import waitroseInvoiceDetail as wid
import pyodbc
import os
from sql.insertSQL import InsertIntoScrubbedStg
from sys import argv

# print(wid(r"W:\Audit\Bacardi\Invoice Images\EmailStagingBay\Waitrose\4700074418.pdf").text)
# print(wid(r"W:\Audit\Bacardi\Invoice Images\EmailStagingBay\Waitrose\4700074418.pdf").Quantity())

script,Salitix_Client_Number = argv

print(Salitix_Client_Number)

exceptions = []

Client_code_dic={'Ab_Inbev':"CL023", 'AG_Barr':"CL005", 'Bacardi':"CL001",
    'Burtons':"CL003", 'Coty':"CL027",'Finsbury_Foods':"CL014",
    'Foxs':"CL999", 'Heineken':"CL028", 'Kettle Foods':"CL026", 
    'Kinnerton':"CL022", 'Maxxium':"CL012", 'Pladis':"CL002", 
    'Premier_Foods':"CL020", 'Princes':"CL029", 'Tilda':"CL013", 'Youngs':"CL004",
    'Loreal':'CL031'}

folder_path = r"W:\Audit\{}\Invoice Images\EmailStagingBay\Waitrose".format(Salitix_Client_Number)
new_folder_path = r"W:\Audit\{}\Invoice Images".format(Salitix_Client_Number)

for file in os.listdir(folder_path):
    # print(wid(os.path.join(folder_path, file)).Product_No())
    print(f"Processing {file}")
    detail = wid(os.path.join(folder_path, file)).All_Detail()
    # print(detail)
    # print(wid(os.path.join(folder_path, file)).text)
    # Rename with the Invoice Number
    if os.path.exists(os.path.join(folder_path, detail['Invoice_Number']+'.pdf')):
        os.rename(os.path.join(folder_path, file),os.path.join(folder_path, detail['Invoice_Number']+'.pdf'))
    else:
        os.replace(os.path.join(folder_path, file),os.path.join(folder_path, detail['Invoice_Number']+'.pdf'))
        # print(detail)
    print(f"Renamed {file} to {detail['Invoice_Number']+'.pdf'}")
    print(detail['Invoice_Date'])
    if detail['Invoice_Date'] is None : 
        if os.path.exists(os.path.join(new_folder_path, detail['Invoice_Number']+'.pdf')):
            os.remove(os.path.join(folder_path, file))
            continue
        elif os.path.exists(os.path.join(folder_path, file)):
            os.rename(os.path.join(folder_path, file),os.path.join(new_folder_path, detail['Invoice_Number']+'.pdf'))
            continue
        else:
            continue
    for i in range(len(detail['Net_Amount'])):
        InsertIntoScrubbedStg(
            Salitix_client_number = Client_code_dic[Salitix_Client_Number],
            SAL_Invoice_Type = detail['SAL_Invoice_Type'],
            Unit_Funding_Type = detail['Unit_Funding_Type'],
            Deal_Type = detail['Deal_Type'],
            Invoice_No = detail['Invoice_Number'],
            Invoice_Date = detail['Invoice_Date'],
            Promotion_No = detail['Promotion_No'],
            Product_No = None if detail['Product_No'] is None else detail['Product_No'][i],
            Start_Date = detail['Invoice_Date'] if detail['Start_Date'] is None else detail['Start_Date'][0],
            End_Date = detail['Invoice_Date'] if detail['End_Date'] is None else detail['End_Date'][0],
            Quantity = None if detail['Quantity'] is None else detail['Quantity'][i],
            Unit_Price = None if detail['Unit_Price'] is None else detail['Unit_Price'][i],
            Net_Amount = detail['Net_Amount'][i],
            VAT_Rate = str(float(detail['Net_Amount'][i])*0.2) if detail['VAT_Amount'] == '20' else '0',
            Gross_Amount = str(float(detail['Net_Amount'][i])*1.2) if detail['VAT_Amount'] == '20' else '0',
            Store_Format = detail['Store_Format'].replace(',','').replace("'","")
        )
                # Move the file from Email Staging Bay to normal folder
        print(f"Moving {file} to {new_folder_path}")
    if os.path.exists(os.path.join(new_folder_path, detail['Invoice_Number']+'.pdf')):
        os.remove(os.path.join(folder_path, detail['Invoice_Number']+'.pdf')) # file))
    elif os.path.exists(os.path.join(folder_path, file)):
        os.rename(os.path.join(folder_path, file),os.path.join(new_folder_path, detail['Invoice_Number']+'.pdf'))
    else:
        print(f"Error Inserting Into Scrubbing {file}")
    # except Exception as e:
    #     print(f"Error Inserting Into Scrubbing {file}")
    #     print(e)
    #     if os.path.exists(os.path.join(new_folder_path,  detail['Invoice_Number']+'.pdf')):
    #         os.remove(os.path.join(folder_path, file))
    #     elif os.path.exists(os.path.join(folder_path, file)):
    #         os.rename(os.path.join(folder_path, file),os.path.join(new_folder_path,  detail['Invoice_Number']+'.pdf'))
    #     exceptions.append(file)

# Run the ftd procedure
conn = pyodbc.connect('DRIVER=SQL Server;SERVER=UKSALAZSQL;DATABASE=Salitix_Master_Data;Trusted_Connection=Yes;UID=SALITIX\SQLSalitixAuditorUsers')
cursor = conn.cursor()

SQL_Query = "EXEC [Salitix_Scrubbed_Data_Formatted].[dbo].[Format_Scrubbed_Charges]"
print('Running "EXEC [Salitix_Scrubbed_Data_Formatted].[dbo].[Format_Scrubbed_Charges]"')

cursor.execute(SQL_Query)
conn.commit()
conn.close()

Salitix_Client_Number = Client_code_dic[Salitix_Client_Number]
# Client_code_dic[client]
Salitix_Customer_Number='WAI01'
# Retailer_Code_dic[retailer]

conn = pyodbc.connect('DRIVER=SQL Server;SERVER=UKSALAZSQL;DATABASE=Salitix_Master_Data;Trusted_Connection=Yes;UID=SALITIX\SQLSalitixAuditorUsers')
cursor = conn.cursor()

SQL_Query = f"EXEC [Salitix_Master_Data].[dbo].[prc_Run_SCC_Load_Scrubbed_Customer_Charges_DTL] {Salitix_Client_Number}, {Salitix_Customer_Number}"

print(SQL_Query)

cursor.execute(SQL_Query)
conn.commit()
conn.close()

# print(exceptions)