import sys
from time import sleep
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


def get_selected_worksheet(sheet, month):
    """
    Return data for selected sheet purchases/sales for a given month
    """
    if sheet == "purchases":
        sheet = PURCHASES_SHEET
    else:
        sheet = SALES_SHEET

    data = sheet.worksheet(month)
    values = data.get_all_values()
    return values


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


def request_input_from_user():
    """
    Ask the user to make a selection
    """
    user_choice = input("\nPlease make a selection:\n")
    return user_choice


def print_selected_menu(menu, heading, menu_options):
    """
    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet
    """
    choice = None
    while choice not in menu_options:
        print('\n' + '*'*70)
        print(f"\n\t{heading}")
        print('\n' + '*'*70)
        print("")
        print("Select")
        print("")
        for k, v in menu_options.items():
            print(f"\t{k} - {v}")
        print("")
        choice = request_input_from_user()

    return (menu, choice.lower(), menu_options)


def print_main_menu():
    """
    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet
    """
    main_menu_options = {
        "1": "Sales",
        "2": "Purchases",
        "x": "Exit"
    }

    heading = "Purchases and sales VAT calculator for self assessment"
    date, time = get_current_date_and_time()
    print(f"\n{date} - {time}")

    return print_selected_menu("main_menu", heading, main_menu_options)


def print_sales_menu():
    """
    Prints a menu of options relating to the sales sheet for a user wish to choose from
    """
    sales_menu_options = {
        "1": "Update sales sheet",
        "2": "Print entire sheet",
        "x": "Return to main menu"
    }

    heading = "Sales menu options"

    return print_selected_menu("sales_menu", heading, sales_menu_options)


def print_purchases_menu():
    """
    Prints a menu of options relating to the purchases sheet for a user wish to choose from
    """
    purchases_menu_options = {
        "1": "Update purchases sheet",
        "2": "Print entire sheet",
        "x": "Return to main menu"
    }

    heading = "Purchases menu options"

    return print_selected_menu("purchases_menu", heading, purchases_menu_options)


def handle_main_menu_choices(choice, menu_options):

    if choice in menu_options:
        if choice == "x":
            print("Exiting program, goodbye...")
            sleep(3)
            sys.exit(0)

        else:
            month = get_month()
            selection = menu_options[choice].lower()

            if selection == "purchases":
                print_purchases_menu()
            elif selection == "sales":
                print_sales_menu()


def main():
    """
    Main function
    """
    menu, choice, menu_options = print_main_menu()

    if menu == "main_menu":
        handle_main_menu_choices(choice, menu_options)



                # break
                # return_values = get_selected_worksheet(selection, month)
        # print(f"\n\n{return_values}\n\n")
            # break
    # show_details_on_vat()
    # date, time = get_current_date_and_time()

main()