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
    green = Fore.GREEN
    red = Fore.RED
    white = Fore.WHITE
    yellow = Fore.YELLOW
    magenta = Fore.MAGENTA


class sales_columns:
    date = 1
    details = 2
    invoice_number = 3
    total = 4
    vat_23 = 5
    vat_13_5 = 6
    vat = 7
    exempt = 8



class purchases_columns:
    date = 1
    details = 2
    invoice_number = 3
    total = 4
    resale_vat = 5
    non_resale_vat = 6
    intra_eu = 7
    vat = 8



# functions for handling output/input
def clear_screen():
    """
    Function to clear the screen so newly display data can be more easily read
    """
    os.system('clear')


def typewriter_print(print_statement, sleep_time=0.03):
    """
    Function to output text to mimic typewriter output speeds
    """
    for char in print_statement:
        sleep(sleep_time)
        sys.stdout.write(char)
        sys.stdout.flush()

    print()


def print_banner(banner):
    """
    Displays a passed banner using Art package
    """
    print('\n' + f'{colors.blue}*'*84)
    print(f"\n\t{text2art(banner)}")
    print('\n' + f'{colors.blue}*'*84)
    print("")


def click_to_continue():
    """
    Request a user press enter to continue, used in a few places so
    broken out to a function for consistent display across the app
    """
    input(f"\n\n\t{colors.yellow}Press Enter to continue: ")


def print_selected_menu(heading, menu_options):
    """
    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet.
    Reprint the menu if a user doesn't select a valid option

    Returns: choice
    """

    clear_screen()
    print_banner(heading)

    print("Select")
    print("")
    for k, v in menu_options.items():
        print(f"\t{k: >2} - " + f"{colors.blue}{v}")
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

    click_to_continue()


def display_message(message, wait_time=None, is_warning=True):
    """
    Request user enters a numeric value
    """
    if is_warning:
        print(f"\n\n\t" + f"{colors.red}{message}\n")
    else:
        print(f"\n\n\t" + f"{colors.green}{message}\n")

    if wait_time:
        sleep(wait_time)
    else:
        click_to_continue()


def display_wait_message(wait_message):
    """
    Displays a wait message to keep a user engaged while data is retrieved
    """
    print(f"{colors.blue}\n  ,,")
    print(f"{colors.blue}c(_)'", end=" ")
    typewriter_print(f"{wait_message}...\n\n")


def get_selected_worksheet(sheet):
    """
    Return data for selected sheet purchases/sales for a given month
    """
    if sheet == "purchases":
        sheet = PURCHASES_SHEET
    else:
        sheet = SALES_SHEET

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


def request_user_select_a_month(sheet):
    """
    Function to request a user selects a month from available months
    """
    month = input("\nPlease select a month to review " + f"{colors.green}(Press L to list available months): ")
    month = month.strip().lower().capitalize()

    months = get_list_of_all_sheet_titles(sheet)

    if month.startswith("L"):
        print(months)
        month = input("\nPlease make a selection: ")
        month = month.strip().lower().capitalize()

    if month in months:
        display_wait_message("This might take a few seconds")

    return (month, months)


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
    print_banner("Add new sale")

    print("Please provide details of the new sales transaction here:\n\n")

    # Questions as variables so size can be determined to neatly display output
    details_q = "Details"
    totals_q = "Total including VAT:"
    vat_rate_q = "Which VAT rate applies? (Press Enter for more details)"

    width = get_length_of_longest_list_item([details_q, totals_q, vat_rate_q])

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
            display_message("Please check that the total price is a number", 0)
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
            display_message("Please check this is a valid tax rate", 2)
            show_details_on_vat()
            request_new_sales_transaction(details=details, price_including_vat=total_price_including_vat)


    return (details, total_price_including_vat, vat_rate)


def calculate_vat(total_price_including_vat, vat_rate):
    """
    Calculate appropriate vat and return a comma separated string for
    updating the google sheet
    """
    vat_applicable = round(((float(total_price_including_vat) * float(vat_rate)) / 100), 2)

    if vat_rate == "23":
        return [vat_applicable, 0, vat_applicable, 0]

    elif vat_rate == "13.5":
        return [0, vat_applicable, vat_applicable, 0]

    elif vat_rate == "0":
        return [0, 0, 0, total_price_including_vat]


def generate_next_invoice_number(ledger):
    """
    Function to get the last available invoice number on a google sheet and iterates it by 1
    """

    all_months = get_list_of_all_sheet_titles(ledger)
    number_of_available_months = len(all_months)
    all_months = reversed(all_months)

    for month in all_months:
        all_data = ledger.worksheet(month).get_all_values()

        last_row = all_data[-1]

        # subtracting 1 below to account for gspread column v list numbering
        last_invoice_number = last_row[sales_columns.invoice_number - 1]

        try:
            if str(last_invoice_number).isnumeric:
                # return last invoice number + 1 (next available)
                return int(last_invoice_number) + 1
        except ValueError as e:
            pass


def create_sheet_if_not_available(sheet):
    """
    Function to check if a sheet for a particular month is
    available, and direct a user to create one if necessary.
    """
    month = get_month()
    available_months = get_list_of_all_sheet_titles(sheet)

    if month not in available_months:
        display_message(f"No sheet available for {month}", 1)
        create_new_sheet(sheet)


def add_new_transaction(sheet):
    """
    Function to add a new transaction to a worksheet.
    This function checks if a sheet for the current month is available &
    generates it if necessary
    """
    ledger = get_selected_worksheet(sheet)

    create_sheet_if_not_available(sheet)

    if sheet == "purchases":
        request_new_purchases_transaction()
    else:
        details, total_price_including_vat, vat_rate = request_new_sales_transaction()
        date, time = get_current_date_and_time()
        invoice_number = generate_next_invoice_number(ledger)
        if invoice_number is None or invoice_number == "":
            invoice_number = input(f"{colors.red}\n\tNo invoice number available, please manually enter one: {colors.white}")
        formatted_vat_details = calculate_vat(total_price_including_vat, vat_rate)

        formatted_row = [date, details,invoice_number,total_price_including_vat] + formatted_vat_details

        try:
            month = get_month()
            ledger.worksheet(month).append_row(formatted_row)
            display_message("Sheet updated successfully", 2, False)

        except FileNotFoundError as e:
            display_message(f"Can't find file: {e}", 3)

        sub_menu(sheet)


def display_all_transactions_for_month(sheet, month=None):
    """
    Function to display google worksheet to the terminal for inspection purposes
    This function tracks the largest item in each column to provide a correctly
    formatted table.
    """
    ledger = get_selected_worksheet(sheet)
    if month is None:
        month = get_month()

    num_of_rows = len(ledger.worksheet(month).col_values(1))
    num_of_cols = len(ledger.worksheet(month).row_values(1))

    columns = []

    for i in range(num_of_cols):
        new_list = ledger.worksheet(month).col_values(i + 1)
        columns.insert(i, new_list)

    print(f"\n{colors.magenta}{month}")
    print(f"{colors.blue}-" * 80)

    dont_color = True

    for idx, i in enumerate(range(num_of_rows)):
        # enumerating of rows and only colouring the first row of headings
        # for greater readability
        dont_color = (idx >= 1)
        for y in range(num_of_cols):
            width = get_length_of_longest_list_item(columns[y])
            column_width = width - len(columns[y][i])
            if not dont_color:
                print(f"{colors.blue}{columns[y][i]}" + " "*column_width, end=" | ")

            else:
                print(f"{columns[y][i]}" + " "*column_width, end=" | ")
        print()

    click_to_continue()


def get_list_of_all_sheet_titles(sheet):
    """
    Returns a list of all sheet titles/available months
    """

    ledger = get_selected_worksheet(sheet)
    all_sheets = ledger.worksheets()
    months = []

    for sheet in all_sheets:
        months.append(sheet.title)

    return months


def display_all_transactions_for_a_selected_month(sheet):
    """
    Function to request a user to select a month to view details of
    in the terminal.
    """
    month, months = request_user_select_a_month(sheet)

    if month in months:
        try:
            display_all_transactions_for_month(sheet, month)
        except FileNotFoundError as e:
            display_message(f"Worksheet not found for chosen month: {e}")

    else:
        print(f"\nAvailable months: {colors.green}{months}")
        display_message(f"Worksheet not found for chosen month, returning to {sheet} menu!", 3)
        clear_screen()
        sub_menu(sheet)


def create_new_sheet(sheet):
    """
    Function to create a new sheet for the current month or a given month.
    """
    all_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    headings = ["Date",	"Details", "Invoice Number", "Total", "Vat 23%", "Vat 13.5%", "VAT", "Exempt or export"]
    response = input("\n\tAdd a sheet for the current month? (n to create for another)" + f"{colors.green} (y/n):  ")
    response = response.lower().strip()

    if response.startswith("y"):
        month = get_month()
        ledger = get_selected_worksheet(sheet)

        try:
            ledger.add_worksheet(month, rows=150, cols=10)
            ledger.worksheet(month).append_row(headings)
            ledger.worksheet(month).format("A1:H1", { 'backgroundColor': {
                'blue': 0.65882355,
                'green': 0.84313726,
                'red': 0.7137255
            }})
            display_message(f"Worksheet created for {month}", 2, False)
        except FileExistsError as e:
            print(f"File already exists: \n{e}")

    elif response.startswith("n"):
        months = get_list_of_all_sheet_titles(sheet)
        print(f"\n\t{colors.green}Already created: " + f"\n\t{colors.white}{months}\n")
        new_month = input("\n\tWhich month would you like to add?  ")
        new_month = new_month.strip().lower().capitalize()

        if new_month not in months and new_month in all_months:
            ledger = get_selected_worksheet(sheet)

            try:
                ledger.add_worksheet(new_month, rows=150, cols=10)
                ledger.worksheet(new_month).append_row(headings)
                ledger.worksheet(new_month).format("A1:H1", { 'backgroundColor': {
                    'blue': 0.65882355,
                    'green': 0.84313726,
                    'red': 0.7137255
            }})
                display_message(f"Worksheet created for {new_month}", 2, False)

            except FileNotFoundError as e:
                print(f"Can't find file:\n{e}")
        else:
            display_message("Please check the value you entered!")
            if sheet in ["sales", "purchases"]:
                sub_menu(sheet)
            else:
                main_menu()

    else:
        display_message("Please check the value you selected!")


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
        sub_menu("sales")

    if choice == "2":
        sub_menu("purchases")

    if choice == "x":
        clear_screen()
        print_banner("Goodbye...")
        sleep(2)
        sys.exit(0)


def user_selected_month_from_available_months(sheet):
    """
    Function to request a user to select a month from available
    months to review transaction totals.
    """
    available_months = get_list_of_all_sheet_titles(sheet)

    if len(available_months) > 0:
        month = None
        while month not in available_months:
            print(f"\nAvailable months: {colors.green}{available_months}")
            month = input("\nPlease enter a month from the available options: ")
            month = month.strip().lower().capitalize()

        if month in available_months:
            display_wait_message("This might take a few seconds")

        return month

    else:
        display_message("No months a currently available, please add one first", 3)
        totals_menu(sheet)


def calculate_total_of_totals_year_to_date(sheet, run_directly=False):
    all_months = get_list_of_all_sheet_titles(sheet)

    totals = []
    vat_23 = []
    vat_13_5 = []
    vat_total = []
    exempt_total = []

    sales_dict = {
        "total": totals,
        "vat_23": vat_23,
        "vat_13.5": vat_13_5,
        "vat_total": vat_total,
        "exempt_total": exempt_total
    }

    sales_headings_dict = {
        "total": "Sales",
        "vat_23": "23% VAT",
        "vat_13.5": "13.5% VAT",
        "vat_total": "VAT",
        "exempt_total": "VAT exempt",
    }

    purchases_dict = {
        "total": totals,
        "vat_23": vat_23,
        "vat_13.5": vat_13_5,
        "vat_total": vat_total,
        "exempt_total": exempt_total
    }

    if sheet == "sales":
        choices_dict = sales_dict
        headings_dict = sales_headings_dict

    else:
        choices_dict = purchases_dict


    for choice in choices_dict.keys():
        sleep(10)
        for month in all_months:
            sleep(3)
            message, month, rounded_total = get_monthly_total_for(sheet, choice, month)
            choices_dict[choice].append(rounded_total)

    print(f"\n{colors.magenta}{sheet.capitalize()} year-to-date totals")
    print(f"{colors.blue}-" * 80)
    # dict_keys_list = list(choices_dict.keys())
    # widths = [(len(key) + 4) for key in dict_keys_list]

    for idx, k in enumerate(choices_dict.keys()):
        # message_width = widths[idx] - len(k)
        print(f"{colors.green}{headings_dict[k]:<16}", end="")
    print()

    for idx, (k, v) in enumerate(choices_dict.items()):
        # message_width = widths[idx] - len(str(v))
        print(f"{colors.blue}€{sum(v):<15.2f}", end="")

    print("\n")

    # avoid needing to click to continue twice when this is run as part of totals menu option 7
    if run_directly:
        click_to_continue()


def print_all_monthly_totals_on_individual_lines(sheet):
    """

    """
    all_months = get_list_of_all_sheet_titles(sheet)

    for month in all_months:
        print_monthly_totals_on_one_line(sheet, month, print_all_months=True)
        # sleep added here to slow down api usage as the program was experiencing
        # -APIError: [429]: Quota exceeded for quota metric 'Read requests'
        #   and limit 'Read requests per minute per user
        sleep(10)

    calculate_total_of_totals_year_to_date(sheet) # todo: keep this (slow)
    click_to_continue()


def print_monthly_totals_on_one_line(sheet, month=None, print_all_months=False):
    """

    """
    choices = ["total", "vat_23", "vat_13.5", "vat_total", "exempt_total"]
    messages = []
    months = []
    rounded_totals = []

    if month == None:
        month = user_selected_month_from_available_months(sheet)

    for choice in choices:
        message, month, rounded_total = get_monthly_total_for(sheet, choice, month)
        messages.append(message)
        months.append(month)
        rounded_totals.append(rounded_total)

    print(f"\n{colors.magenta}{months[0]} totals")
    print(f"{colors.blue}-" * 80)
    # widths = [(len(message) + 4) for message in messages]

    for idx, message in enumerate(messages):
        # message_width = widths[idx] - len(message)
        print(f"{colors.green}{message:<16}", end="")
    print()

    for idx, rounded_total in enumerate(rounded_totals):
        # message_width = (widths[idx]- 1) - len(str(rounded_total))
        print(f"{colors.white}€{rounded_total:<15.2f}", end="")

    # print("\n\n" + f"{colors.blue}-" * 80)

    if not print_all_months:
        print("\n")
        click_to_continue()

    else:
        print()


def get_monthly_total_for(sheet, choice, month=None):
    """

    """
    message = ""
    column = ""

    if sheet == "sales":
        if choice == "total":
            message = "Sales"
            column = sales_columns.total
        elif choice == "vat_23":
            message = "23% VAT"
            column = sales_columns.vat_23
        elif choice == "vat_13.5":
            message = "13.5% VAT"
            column = sales_columns.vat_13_5
        elif choice == "vat_total":
            message = "VAT"
            column = sales_columns.vat
        elif choice == "exempt_total":
            message = "VAT exempt"
            column = sales_columns.exempt

    else:
        column = purchases_columns.date
        column = purchases_columns.details
        column = purchases_columns.invoice_number
        column = purchases_columns.total
        column = purchases_columns.resale_vat
        column = purchases_columns.non_resale_vat
        column = purchases_columns.intra_eu
        column = purchases_columns.vat

    if month is None:
        month = user_selected_month_from_available_months(sheet)

    ledger = get_selected_worksheet(sheet)

    totals_without_header = ledger.worksheet(month).col_values(column)[1:]

    combined_total = sum([float(total) for total in totals_without_header])
    rounded_total = round(float(combined_total), 2)

    return (message, month, rounded_total)


def get_total_for_all_months(column, sheet):
    months = get_list_of_all_sheet_titles(sheet)

    messages = []
    all_months = "'all months'"
    rounded_totals = []

    for month in months:
        message, month, rounded_total = get_monthly_total_for(sheet, column, month)
        messages.append(message)
        rounded_totals.append(rounded_total)

    return (messages[0], all_months, sum(rounded_totals))


def totals_menu(sheet):
    """
    Calls the generic print selected_menu function with
    totals specific options for a user to interogate the
    data for a given month
    """

    menu = "totals menu"
    heading = f"{sheet.capitalize()} totals"
    totals_menu_options = {
        "1": "Month: Display all totals",
        "2": f"Month: {sheet.capitalize()} (including VAT)",
        "3": "Month: VAT (23%)",
        "4": "Month: VAT (13.5%)",
        "5": "Month: VAT (combined)",
        "6": f"Month: Tax exempt {sheet}",
        "7": "Year-to-date: Display all totals",
        "8": "Year-to-date: Display totals",
        "9": f"Year-to-date: {sheet.capitalize()} (including VAT)",
        "10": "Year-to-date: VAT (23%)",
        "11": "Year-to-date: VAT (13.5%)",
        "12": "Year-to-date: Total VAT (combined)",
        "13": f"Year-to-date: Tax exempt {sheet}",
        "x": f"Back to {sheet} menu"
    }

    choice = print_selected_menu(heading, totals_menu_options)

    if choice == "1":
        print_monthly_totals_on_one_line(sheet)
        totals_menu(sheet)

    if choice == "2":
        message, month, rounded_total = get_monthly_total_for(sheet, "total")
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "3":
        message, month, rounded_total = get_monthly_total_for(sheet, "vat_23")
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "4":
        message, month, rounded_total = get_monthly_total_for(sheet, "vat_13.5")
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "5":
        message, month, rounded_total = get_monthly_total_for(sheet, "vat_total")
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "6":
        message, month, rounded_total = get_monthly_total_for(sheet, "exempt_total")
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "7":
        display_wait_message("This will take a few minutes")
        print_all_monthly_totals_on_individual_lines(sheet)
        totals_menu(sheet)

    if choice == "8":
        display_wait_message("This will take a few minutes")
        calculate_total_of_totals_year_to_date(sheet, run_directly=True)
        totals_menu(sheet)

    if choice == "9":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("total", sheet)
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "10":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("vat_23", sheet)
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "11":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("vat_13.5", sheet)
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "12":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("vat_total", sheet)
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "13":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("exempt_total", sheet)
        display_message(f"{message} for {month}: {colors.white}€{rounded_total:.2f}", is_warning=False)
        totals_menu(sheet)

    if choice == "x":
        if sheet == "sales":
            sub_menu(sheet)
        else:
            purchases_menu()


def sub_menu(sheet):
    """
    Calls the generic print_selected_menu function with
    sub_menu specific options, heading, and handles
    user input
    """

    menu_options = {
        "1": "Add a new transaction",
        "2": "Display all transactions for the current month",
        "3": "Display all transactions for a given month",
        "4": "Create a new sales sheet for the current month (if none yet exists)",
        "5": "Show details on local VAT rates",
        "6": "Display 'Totals' menu",
        "x": "Return to main menu"
    }

    choice = print_selected_menu(sheet.capitalize(), menu_options)

    if choice == "1":
        add_new_transaction(sheet)
    if choice == "2":
        display_wait_message("This might take a few seconds")
        display_all_transactions_for_month(sheet)
        sub_menu(sheet)
    if choice == "3":
        display_all_transactions_for_a_selected_month(sheet)
        sub_menu(sheet)
    if choice == "4":
        create_new_sheet(sheet)
        sub_menu(sheet)
    if choice == "5":
        show_details_on_vat()
        sub_menu(sheet)
    if choice == "6":
        totals_menu(sheet)

    if choice == "x":
        main_menu()


def main():
    """
    Main function
    """
    try:
        main_menu()
    except Exception:
        raise ("Something went wrong, try rebooting")

main()
