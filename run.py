import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
PURCHASES_SHEET = GSPREAD_CLIENT.open('vat_purchases')
SALES_SHEET = GSPREAD_CLIENT.open('vat_sales')

purchases = PURCHASES_SHEET.worksheet("January")
sales = SALES_SHEET.worksheet("January")

purchases_data = purchases.get_all_values()
print("\npurchases_data:")
print(purchases_data)

sales_data = sales.get_all_values()
print("\nsales_data:")
print(sales_data)
