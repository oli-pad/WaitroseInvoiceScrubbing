import pdfplumber
import re

Dictionary = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12"
}

class waitroseInvoiceDetail:
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = self.pdf_to_text()    

    def __str__(self):
        return self.filepath
    
    def pdf_to_text(self):
        with pdfplumber.open(self.filepath) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    def invoice_number(self):
        match = re.search(r'Invoice Number: (\d+)', self.text)
        return match.group(1) if match else re.search(r'Credit Memo Number: (\d+)', self.text).group(1)
    
    def SAL_Invoice_type(self):
        if self.Deal_Type() == 'Non-Promotional':
            return 'MS'
        else:
            return 'PR'

    def Unit_Funding_Type(self):
        if self.Deal_Type() == 'Non-Promotional':
            return None
        else:
            return 'E'

    def Line_Description(self):
        pass

    def Deal_Type(self):
        match = re.search(r'Retro, ', self.text)
        match2 = re.search(r'Multivalue, ', self.text)
        if match:
            return 'Retro'
        elif match2:
            return 'Multivalue'
        else:
            return 'Non-Promotional'

    def Invoice_Date(self):
        match = re.search(r'Invoice Date : (\d{2})-(.*)-(\d{4})', self.text)
        return f'{match.group(3)}-{Dictionary[match.group(2)]}-{match.group(1)}' if match else None

    def Promotion_No(self):
        match = re.search(r'Promotion: [(](\d+)[)]', self.text)
        return match.group(1) if match else None

    def Product_No(self):
        # if self.Deal_Type() == 'Retro':
        #     matches = re.findall(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d+) (.*) (\d+) ([0-9,.]*)', self.text)
        #     return [match[6] for match in matches] if matches else None
        if self.Deal_Type() in ['Multivalue','Retro']:
            list=[]
            status=False
            for line in self.text.split("\n"):
                if status:
                    if re.search(r'(\d*) (.*) (\d+) (\d+)',line):
                        list.append(re.search(r'(\d*) (.*) (\d+) (\d+)',line).group(1))
                if re.search(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',line):
                    list.append(re.search(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',line).group(7))
                    status=True
            return list
        else:
            matches = re.findall(r'(\d+) (.*) (\d+) (.*) (\d{2})/(\d{2})/(\d{4}) (\d{2})/(\d{2})/(\d{4}) ([0-9.,]*) ([0-9.,]*) £([0-9.,]*)', self.text)
            return [match[2] for match in matches] if matches else None

    def Start_Date(self):
        # if self.Deal_Type() == 'Retro':
        #     matches = re.findall(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d+) (.*) (\d+) ([0-9,.]*)', self.text)
        #     return [match[2]+"-"+match[1]+"-"+match[0] for match in matches] if matches else None
        if self.Deal_Type() in ['Multivalue','Retro']:
            matches = re.findall(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',self.text)
            return [match[2]+"-"+match[1]+"-"+match[0] for match in matches] if matches else None
        else:
            matches = re.findall(r'(\d+) (.*) (\d+) (.*) (\d{2})/(\d{2})/(\d{4}) (\d{2})/(\d{2})/(\d{4}) ([0-9.,]*) ([0-9.,]*) £([0-9.,]*)', self.text)
            return [match[6]+"-"+match[5]+"-"+match[4] for match in matches] if matches else None

    def End_Date(self):
        # if self.Deal_Type() == 'Retro':
        #     matches = re.findall(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d+) (.*) (\d+) ([0-9,.]*)', self.text)
        #     return [match[5]+"-"+match[4]+"-"+match[3] for match in matches] if matches else None
        if self.Deal_Type() in ['Multivalue','Retro']:
            matches = re.findall(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',self.text)
            return [match[5]+"-"+match[4]+"-"+match[3] for match in matches] if matches else None
        else:
            matches = re.findall(r'(\d+) (.*) (\d+) (.*) (\d{2})/(\d{2})/(\d{4}) (\d{2})/(\d{2})/(\d{4}) ([0-9.,]*) ([0-9.,]*) £([0-9.,]*)', self.text)
            return [match[9]+"-"+match[8]+"-"+match[7] for match in matches] if matches else None
    
    def Quantity(self):
        if self.Deal_Type() == 'Retro':
            matches = re.findall(r'Retro, (\d+) Units x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            if len(matches) == 0:
                matches = re.findall(r'Retro, (.*) Cases x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
                if len(matches) == 0:
                    list=[]
                    status=False
                    for line in self.text.split("\n"):
                        if status:
                            if re.search(r'(\d*) (.*) (\d+) (\d+)',line):
                                list.append(re.search(r'(\d*) (.*) (\d+) (\d+)',line).group(3))
                        if re.search(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',line):
                            list.append(re.search(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',line).group(9))
                            status=True
                    return list
            return [float(match[10].replace(",",""))/float(match[1]) for match in matches]
        elif self.Deal_Type() == 'Multivalue':
            matches = re.findall(r'Multivalue, (\d+) triggers x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            if len(matches) == 0:
                list=[]
                status=False
                for line in self.text.split("\n"):
                    if status:
                        if re.search(r'(\d*) (.*) (\d+) (\d+)',line):
                            list.append(re.search(r'(\d*) (.*) (\d+) (\d+)',line).group(3))
                    if re.search(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',line):
                        list.append(re.search(r'(\d{2})[.](\d{2})[.](\d{4}) (\d{2})[.](\d{2})[.](\d{4}) (\d*) (.*) (\d+) (\d+)',line).group(9))
                        status=True
                return list
            return [float(match[10].replace(",",""))/float(match[1]) for match in matches]
        else:
            matches = re.findall(r'(\d+) (.*) (\d+) (.*) (\d{2})/(\d{2})/(\d{4}) (\d{2})/(\d{2})/(\d{4}) ([0-9.,]*) ([0-9.,]*) £([0-9.,]*)', self.text)
            return [match[10] for match in matches] if matches else None

    def Unit_Price(self):
        if self.Deal_Type() == 'Multivalue':
            matches = re.findall(r'Multivalue, (\d+) triggers x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            return [float(match[1]) for match in matches]
        elif self.Deal_Type() == 'Retro':
            matches = re.findall(r'Retro, (\d+) Units x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            if len(matches) == 0:
                matches = re.findall(r'Retro, (.*) Cases x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            return [float(match[1]) for match in matches]
        matches = re.findall(r'(\d+) (.*) (\d+) (.*) (\d{2})/(\d{2})/(\d{4}) (\d{2})/(\d{2})/(\d{4}) ([0-9.,]*) ([0-9.,]*) £([0-9.,]*)', self.text)
        return [match[11] for match in matches] if matches else None

    def Net_Amount(self):
        if self.Unit_Price() == None:
            match = re.search(r'(\d+) (.*) (\d+) [(]?([0-9.,]*)[)]? [(]?([0-9.,]*)[)]? ([0-9.]*)', self.text)
            if re.search(r'[(]([0-9,.]*)[)]',self.text):
                return["-"+match.group(5).replace(",","")] if match else None
            return [match.group(5).replace(",","")] if match else None
        elif self.Deal_Type() == 'Multivalue':
            matches = re.findall(r'Multivalue, (\d+) triggers x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            list =  [float(match[10].replace(",","")) for match in matches]
            #remove the element that is = 0
            if matches == 0:
                return [list[i] for i in range(len(list)) if list[i] != 0]
        elif self.Deal_Type() == 'Retro':
            matches = re.findall(r'Retro, (\d+) Units x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            if len(matches) == 0:
                matches = re.findall(r'Retro, (.*) Cases x £ ([0-9,.]*), (\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4}) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',self.text)
            list =  [float(match[10].replace(",","")) for match in matches]
            #remove the element that is = 0
            return [list[i] for i in range(len(list)) if list[i] != 0]
        else:
            matches = re.findall(r'(\d+) (.*) (\d+) (.*) (\d{2})/(\d{2})/(\d{4}) (\d{2})/(\d{2})/(\d{4}) ([0-9.,]*) ([0-9.,]*) £([0-9.,]*)', self.text)
            return [match[12].replace(",","") for match in matches] if matches else None

    def VAT_Amount(self):
        match = re.search(r'(\d+) (.*) (\d+) [(]?([0-9.,]*)[)]? [(]?([0-9.,]*)[)]? ([0-9.]*)', self.text)
        return match.group(6).replace(".00","") if match else None

    def Gross_Amount(self):
        if self.Unit_Price() == None:
            float(self.Net_Amount()[0]) *(1+ float(self.VAT_Amount())/100)
        else:
            return [ float(self.Net_Amount()[i]) *(1+ (float(self.VAT_Amount())/100)) for i in range(len(self.Net_Amount()))] if len(self.Net_Amount())>0 else None

    def Store_Format(self):
        match = re.search(r'(\d+) (.*) (\d+) [(]?([0-9.,]*)[)]? [(]?([0-9.,]*)[)]? ([0-9.]*)', self.text)
        return match.group(2) if match else None

    def Invoice_Description(self):
        pass

    def Acquisition_Ind(self):
        pass

    def All_Detail(self):
        return {
            "Invoice_Number": self.invoice_number(),
            "Invoice_Date": self.Invoice_Date(),
            "Promotion_No": self.Promotion_No(),
            "Product_No": self.Product_No(),
            "Start_Date": self.Start_Date(),
            "End_Date": self.End_Date(),
            "Quantity": self.Quantity(),
            "Unit_Price": self.Unit_Price() if self.Deal_Type() else None,
            "Net_Amount": self.Net_Amount() if self.Deal_Type() else None,
            "VAT_Amount": self.VAT_Amount(),
            "Gross_Amount": self.Gross_Amount(),
            "Store_Format": self.Store_Format(),
            "Deal_Type": self.Deal_Type(),
            "SAL_Invoice_Type": self.SAL_Invoice_type(),
            "Unit_Funding_Type": self.Unit_Funding_Type()
        }
    