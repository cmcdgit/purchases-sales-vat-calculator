import datetime
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


def get_current_purchases_worksheet(month):
    """
    Returns purchases data for a given month
    """
    purchases = PURCHASES_SHEET.worksheet(month)
    purchases_data = purchases.get_all_values()
    return purchases_data


def get_current_sales_worksheet(month):
    """
    Return sales data for a given month
    """
    sales = SALES_SHEET.worksheet(month)
    sales_data = sales.get_all_values()
    return sales_data


def show_details_on_vat():
    """
    Display details on VAT in Ireland
    """

    irish_vat_rates = {
        23: """
        This is the standard VAT rate in Ireland, which applies to most goods
        and services, including electronics, household appliances, clothing,
        and professional services.
        """,
        13.5: """
        This reduced VAT rate applies to certain goods and services, including
        electricity, gas, restaurant services, and building services (e.g.,
        renovation and repair of residential property).
        """,
        9: """
        This lower VAT rate is primarily for tourism and hospitality sectors.
        It applies to services such as hotel accommodation, restaurant meals,
        and admission to cinemas, theaters, museums, and certain sports
        facilities.
        """,
        4.8: """
        This special VAT rate applies exclusively to the supply of
        livestock (cattle, sheep, etc.).
        """,
        0: """
        This zero rate applies to certain essential goods and services,
        such as most food items (except for those subject to the 13.5% rate),
        children's clothing and footwear, oral medicines, and exports.
        """
    }
    print("\n\tPlease check which tax rate applies if you are unsure\n")
    for k, v in irish_vat_rates.items():
        print("\t" + "*"*70)
        print(f"\t{k}%{v}")



def get_current_date_and_time():
    """
    Returns the current date and time to accurately log a transaction.
    """
    now = datetime.datetime.now()

    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")
    return (date, time)


def get_month():
    """
    Returns the current month so the correct spreadsheet can be updated.
    """
    now = datetime.datetime.now()

    month = now.strftime("%B")
    return month


def handle_user_choice(choice, menu_options):
    """
    Determines worksheet to return or whether to exit
    """
    # print(menu_options.keys())

    if choice not in menu_options.keys():
        print("if")
        return False
    else:
        print("else")
        return menu_options[choice]




def request_input_from_user():
    """
    Ask the user to make a selection
    """
    user_choice = input("\nPlease make a selection:\n")
    return user_choice


def print_menu():
    """
    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet
    """
    menu_options = {
        "1": "Sales",
        "2": "Purchases",
        "x": "Exit"
    }

    date, time = get_current_date_and_time()
    print(f"\n{date} - {time}")
    print("\nPurchases and sales VAT calculator for self assessment")
    print("")
    print("Select")
    print("")
    for k, v in menu_options.items():
        print(f"{k} - {v}")
    print("")

    return menu_options


def main():
    """
    Main function
    """
    menu_options = print_menu()
    choice = request_input_from_user()
    return_value = False
    while not return_value:
        return_value = handle_user_choice(choice, menu_options)

    print(return_value)

    # show_details_on_vat()
    # date, time = get_current_date_and_time()
    # print(date)
    # print(time)
    month = get_month()
    # print(month)
    # month = "January"

    # purchases_data = get_current_purchases_worksheet(month)
    # print("\npurchases_data:")
    # print(purchases_data)

    # sales_data = get_current_sales_worksheet(month)
    # print("\nsales_data:")
    # print(sales_data)


main()