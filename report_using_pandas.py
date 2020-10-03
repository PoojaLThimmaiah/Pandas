import pandas as pd
df = pd.read_csv("C:\\Pooja\\Report\\Report_ATB_1104.csv",parse_dates=["Disch Date","Claim Transmission Date","Admit Date","Registration Date","Inpatient Admit Date","Claim Submission Date",
                                                                         "Statement Transmission Date"])
df[["Primary Fin Class","DNFB Status","Current Fin Class","Aging Category",
   "Encounter Class","Encounter Type","Patient Bed","Patient Building","Patient Facility"]]=df[["Primary Fin Class","DNFB Status","Current Fin Class","Aging Category",
   "Encounter Class","Encounter Type","Patient Bed","Patient Building","Patient Facility"]].astype("category")
from datetime import date,timedelta
df["Date"] = date.today() - timedelta(days=1)
df["Date"] = df["Date"].astype("datetime64[ns]")
df["CurDt-TranDt"] = df["Date"] - df["Claim Transmission Date"]
df["Days"] = df["Date"] - df["Disch Date"]
df["Days"] = pd.to_numeric(df["Days"].dt.days, downcast='integer')
def aging_bucket(number):
    if number <=30.0:
        return "A. 0 to 30 days"
    elif number <=60.0:
        return "B. 31 to 60 days"
    elif number <=90.0:
        return "C. 61 to 90 days"
    elif number <=180.0:
        return "D. 90 to 180 days"
    elif number <=365.0:
        return "F. 181 to 365 days"
    else:
        return "G. 366 and above"
column = ["Days"]
for col in column:
    df["Ageing Bucket"]=df[col].apply(aging_bucket)
def Amb_Acute(value):
    if value in ["Medical","Central","Surgery Clinic","Urgent Care"]:
        return "Ambulatory"
    else:
        return "Acute"
for val in ["Patient Facility"]:
    df["Ambulatory/Acute"] = df[val].apply(Amb_Acute)
def Credit_balance(i):
    if i<0:
        return "Credit Balance"
    
    
def client_selfpay(i):
    if i == "Client":
        return "Client"
    elif i == "Self Pay":
        return "Selfpay"
def category1(row):
    AR_Bal = row["Current A/R Balance"]
    finclass = row["Current Fin Class"]
    aging = row["Aging Category"]
    dnfb_stat = row["DNFB Status"]
    
    if AR_Bal < 0:
        return "Credit Bal"
    elif finclass == "Self Pay":
        return "Selfpay"
    elif finclass == "Client":
        return "Client"
    elif aging == "Not Aged":
        return "Not Aged"
    elif aging == "DNFB":
        return "DNFB"
    else:
        return "Insurance"
    
df["Category"]= df.apply(category1,axis="columns")
df1 = df.pivot_table(values="Current A/R Balance", index = ["Ambulatory/Acute","Ageing Bucket"],aggfunc="sum")
writer = pd.ExcelWriter(path = "C:\\Pooja\\Report\\Report_1104 - Worked.xlsx", engine = 'xlsxwriter')
df.to_excel(writer, sheet_name="Worked")
df1.to_excel(writer, sheet_name="Pivot")
writer.save()
writer.close()


