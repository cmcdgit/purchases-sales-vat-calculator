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
# print("\npurchases_data:")
# print(purchases_data)

sales_data = sales.get_all_values()
# print("\nsales_data:")
# print(sales_data)


def get_current_date_and_time():
    """
    Returns the current date and time to accurately log a transaction.
    """
    pass


def get_month():
    """
    Returns the current month so the correct spreadsheet can be updated.
    """
    pass



def print_menu():
    """
    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet
    """
    print("\nPurchases and sales VAT calculator for self assessment")
    print("")
    print("Select")
    print("")
    print("1 - Sales")
    print("2 - Purchases")
    print("")
    print("X - Exit")
    print("")

# todo: confirm if this can serve for all inputted data or might need to be integrated with print_menu()
def request_input_from_user():
    """
    Ask the user to make a selection
    """
    print_menu()
    user_choice = input("\nPlease make a selection:\n")
    print(f"\nYou chose option {user_choice}")


def main():
    """
    Main function
    """
    request_input_from_user()


main()