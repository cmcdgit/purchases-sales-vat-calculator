import sys
import os
from time import sleep
import datetime
import gspread
from google.oauth2.service_account import Credentials
from art import *
from colorama import Fore, Back, Style, init

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
vat_rate = None
total_price_including_vat = None

init()
init(autoreset=True)


class colors:
    blue = Fore.BLUE



class sales_columns:
    date = 0
    details = 1
    invoice_number = 2
    total = 3
    vat_23 = 4
    vat_13_5 = 5
    vat = 6
    exempt = 7



class purchases_columns:
    date = 0
    details = 1
    invoice_number = 2
    total = 3
    resale_vat = 4
    non_resale_vat = 5
    intra_eu = 6
    vat = 7



# functions for handling output/input
def clear_screen():
    """
    Function to clear the screen so newly display data can be more easily read
    """
    os.system('clear')


def typewriter_print(print_statement):
    """
    Function to output text to mimic typewriter output speeds
    """
    for char in print_statement:
        sleep(0.03)
        sys.stdout.write(char)
        sys.stdout.flush()

    print()


def print_selected_menu(heading, menu_options):
    """
    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet.
    Reprint the menu if a user doesn't select a valid option

    Returns: choice
    """

    clear_screen()

    print('\n' + f'{colors.blue}*'*84)
    print(f"\n\t{text2art(heading)}")
    print('\n' + f'{colors.blue}*'*84)
    print("")
    print("Select")
    print("")
    for k, v in menu_options.items():
        print(f"\t{k} - " + f"{colors.blue}{v}")
    print("")

    choice = request_input_from_user()

    while choice not in menu_options:
        print("You have selected an option that does not exist, please try again...")
        sleep(2)
        print_selected_menu(heading, menu_options)
        choice = request_input_from_user()

    return choice


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

    clear_screen()

    typewriter_print("\n\tPlease check which tax rate applies if you are unsure\n")
    for k, v in irish_vat_rates.items():
        print("\t" + "*"*80)
        print(f"{Fore.LIGHTWHITE_EX}\t{k}%" + f"{Fore.BLUE}{v}")
        sleep(1.5)

    input("\n\tPress Enter to continue: ")


def display_error_message(error_message, wait_time):
    """
    Request user enters a numeric value
    """
    print(f"\n\n\t" + f"{Fore.RED}{error_message}\n")

    if wait_time:
        sleep(wait_time)
    else:
        input("\n\tPress Enter to continue: ")


def get_selected_worksheet(sheet):
    """
    Return data for selected sheet purchases/sales for a given month
    """
    if sheet == "purchases":
        sheet = PURCHASES_SHEET
    else:
        sheet = SALES_SHEET

    # data = sheet.worksheet(month)
    # values = data.get_all_values()
    return sheet


def get_current_date_and_time():
    """
    Returns the current date and time (formatted) to accurately log a transaction.
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

    Returns: user_choice in lowercase, and stripped of whitespace
    """
    typewriter_print("\nChoose an option:\n")
    user_choice = input().lower().strip()

    return user_choice


def display_countdown(menu):
    """
    Function to show a countdown for temporarily displayed info.
    """
    counter = 10
    print(f"Returning to the {menu} in {counter} seconds")
    for i in range(counter, -1, -1):
        print("."*i + str(i))
        sleep(1)

    print()


def get_length_of_longest_list_item(list_to_check):
    """
    Returns the longest string in a list of strings,
    useful for formatting out and improving readability
    """
    return len(sorted(list_to_check, key=len, reverse=True)[0])


def request_new_purchases_transaction():
    pass


def request_new_sales_transaction(details=None, price_including_vat=None, rate=None):
    """
    Function to collect the info needed to add a new sales transaction to the google sheet
    """
    global total_price_including_vat
    global vat_rate

    clear_screen()
    new_sale_banner = text2art("Add new sale")


    print('\n' + f'{colors.blue}*'*84)
    print(f"\n\t{new_sale_banner}")
    print('\n' + f'{colors.blue}*'*84)
    print("")
    print("Please provide details of the new sales transaction here:\n\n")

    # Questions as variables so size can be determined to neatly display output
    details_q = "Details"
    totals_q = "Total including VAT:"
    vat_rate_q = "Which VAT rate applies? (Press Enter for more details)"

    # required_space = 4
    width = get_length_of_longest_list_item([details_q, totals_q, vat_rate_q])
    # + required_space

    space = "  "
    formatted_details_q = f"{details_q}" + "."*(width - len(details_q)) + space
    formatted_price_q = f"{totals_q}" + "."*(width - len(totals_q)) + space + "€"
    formatted_vat_rate_q = f"{vat_rate_q}" + "."*(width - len(vat_rate_q)) + space

    vat_rate = rate
    total_price_including_vat = price_including_vat

    if details is None:
        details = input(formatted_details_q)
    else:
        print(formatted_details_q + f"{details}")

    if total_price_including_vat is None:
        total_price_including_vat = input(formatted_price_q)

        try:
            total_price_including_vat = float(total_price_including_vat)

        except ValueError:
            display_error_message("Please check that the total price is a number", 0)
            request_new_sales_transaction(details=details)

    else:
        print(formatted_price_q + str(total_price_including_vat))

    if vat_rate is None:
        vat_rate = input(formatted_vat_rate_q)

        if "%" in vat_rate:
            vat_rate = vat_rate.replace("%", "")

        if vat_rate in ["23", "13.5", "9", "4.8", "0"]:
            pass
        elif vat_rate == None or vat_rate == "":
            show_details_on_vat()
            request_new_sales_transaction(details=details, price_including_vat=total_price_including_vat)
        else:
            display_error_message("Please check this is a valid tax rate", 2)
            show_details_on_vat()
            request_new_sales_transaction(details=details, price_including_vat=total_price_including_vat)

    # else:
    #     print(formatted_vat_rate_q + f"{vat_rate}%")

    return (details, total_price_including_vat, vat_rate)


def calculate_vat(total_price_including_vat, vat_rate):
    """
    Calculate appropriate vat and return a comma separated string for
    updating the google sheet
    """
    vat_applicable = round(((float(total_price_including_vat) * float(vat_rate)) / 100), 2)

    if vat_rate == "23":
        return [vat_applicable, None, vat_applicable, None]

    elif vat_rate == "13.5":
        return [None, vat_applicable, vat_applicable, None]

    elif vat_rate == "0":
        return [None, None, None, total_price_including_vat]


def generate_next_invoice_number(ledger, month):
    """
    Function to get the last invoice number on a google sheet and iterate by 1
    """

    all_data = ledger.worksheet(month).get_all_values()
    last_row = all_data[-1]
    last_invoice_number = last_row[sales_columns.invoice_number]
    if str(last_invoice_number).isnumeric:
        return int(last_invoice_number) + 1


def add_new_transaction(sheet):
    ledger = get_selected_worksheet(sheet)
    month = get_month()

    if sheet == "purchases":
        request_new_purchases_transaction()
    else:
        details, total_price_including_vat, vat_rate = request_new_sales_transaction()
        date, time = get_current_date_and_time()
        invoice_number = generate_next_invoice_number(ledger, month)
        formatted_vat_details = calculate_vat(total_price_including_vat, vat_rate)

        formatted_row = [date, details,invoice_number,total_price_including_vat] + formatted_vat_details

        try:
            ledger.worksheet(month).append_row(formatted_row)
        except FileNotFoundError as e:
            print(f"Can't find file:\n{e}")

        sales_menu()


def edit_transaction(sheet):
    pass


def display_all_transactions_for_current_month(sheet):
    ledger = get_selected_worksheet(sheet)
    month = get_month()

    col_1 = ledger.worksheet(month).col_values(1)
    col_2 = ledger.worksheet(month).col_values(2)
    col_3 = ledger.worksheet(month).col_values(3)
    col_4 = ledger.worksheet(month).col_values(4)
    col_5 = ledger.worksheet(month).col_values(5)
    col_6 = ledger.worksheet(month).col_values(6)
    col_7 = ledger.worksheet(month).col_values(7)
    col_8 = ledger.worksheet(month).col_values(8)

    # all_cols = [row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8]

    for i in range(8):
        print(f"{col_1[i]} | {col_2[i]} | {col_3[i]} | {col_4[i]} | {col_5[i]} | {col_6[i]} | {col_7[i]} | {col_8[i]}")
    # for row in all_rows:
    #     length = get_length_of_longest_list_item(row)

    #     for col in row:
    #         all_cols.append(col)



        # print(length)
        # print(row)

    # print(row_1)
    # print(row_2)
    # print(row_3)
    # print(row_4)
    # print(row_5)
    # print(row_6)
    # print(row_7)
    # print(row_8)

    # for row in all_data:
    #     print(row)
    input("\n\tPress Enter to continue: ")


def display_all_transactions_for_a_selected_month(sheet):
    pass


def create_new_sheet_for_current_month(sheet):
    pass


def main_menu():
    """
    Calls the generic print_selected_menu function with
    main_menu specific options, heading, and handles
    user input
    """

    heading = "VAT Calculator"
    menu_options = {
        "1": "Sales",
        "2": "Purchases",
        "x": "Exit"
    }

    date, time = get_current_date_and_time()
    print(f"\n{date} - {time}")

    choice = print_selected_menu(heading, menu_options)

    if choice == "1":
        sales_menu()
    if choice == "2":
        purchases_menu()


def sales_menu():
    """
    Calls the generic print_selected_menu function with
    sales_menu specific options, heading, and handles
    user input
    """
    sheet = "sales"
    menu = "sales menu"
    heading = "Sales"
    sales_menu_options = {
        "1": "Add a new transaction",
        "2": "Edit a transaction",
        "3": "Display all transactions for the current month",
        "4": "Display last 7 transactions for the current month",
        "5": "Display all transactions for a given month",
        "6": "Create a new sales sheet for the current month (if none yet exists)",
        "7": "Show details on local VAT rates",
        "x": "Return to main menu"
    }

    choice = print_selected_menu(heading, sales_menu_options)

    if choice == "1":
        add_new_transaction(sheet)
    if choice == "2":
        edit_transaction(sheet)
    if choice == "3":
        display_all_transactions_for_current_month(sheet)
        sales_menu()
    if choice == "4":
        display_last_7_transactions_for_current_month(sheet)
    if choice == "5":
        display_all_transactions_for_a_selected_month(sheet)
    if choice == "6":
        create_new_sheet_for_current_month(sheet)
    if choice == "7":
        show_details_on_vat()
        sales_menu()

    if choice == "x":
        main_menu()


def purchases_menu():
    """
    Calls the generic print_selected_menu function with
    purchases_menu specific options, heading, and handles
    user input
     """

    sheet = "purchases"
    menu = "purchases menu"
    heading = "Purchases"
    purchases_menu_options = {
        "1": "Switch to sale menu",
        "7": "Show details on local VAT rates",
        "x": "Return to main menu"
    }

    choice = print_selected_menu(heading, purchases_menu_options)

    if choice == "1":
        sales_menu()

    if choice == "7":
        show_details_on_vat()
        display_countdown(menu)
        purchases_menu()

    if choice == "x":
        main_menu()


def main():
    """
    Main function
    """
    main_menu()


main()
