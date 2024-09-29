# pylint: disable=too-many-lines
"""
This module allows a user to interact with Google sheets using the API
so they can self assess for tax on sales and puchases items at
the point of sale
"""

import sys
import os
from time import sleep
import datetime
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, init

SCOPE = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
PURCHASES_SHEET = GSPREAD_CLIENT.open('vat_purchases')
SALES_SHEET = GSPREAD_CLIENT.open('vat_sales')

# pylint: disable-next=invalid-name
vat_rate = None
# pylint: disable-next=invalid-name
total_price_including_vat = None
# pylint: disable-next=invalid-name
choice = None

init()
init(autoreset=True)


class Colors:
    """Colorama Colors class

    Class for Colors so they can be accessed using dot notation
    for consistency.
    """

    blue = Fore.BLUE
    green = Fore.GREEN
    red = Fore.RED
    white = Fore.WHITE
    yellow = Fore.YELLOW
    magenta = Fore.MAGENTA


class Columns:
    """Columns class

    Class for columns so they can be accessed using dot notation
    for consistency.
    """

    date = 1
    details = 2
    invoice_number = 3
    total = 4
    vat_23 = 5
    vat_13_5 = 6
    vat_9 = 7
    vat = 8
    exempt = 9


# functions for handling output/input
def clear_screen():
    """Clear screen

    Function to clear the screen so newly display data can
    be more easily read.
    """

    os.system('clear')


def typewriter_print(print_statement, sleep_time=0.03):
    """Enumlate typewriter output

    Function to output text to mimic typewriter output speeds
    uses a default sleep_time which can be overridden.
    """

    for char in print_statement:
        sleep(sleep_time)
        sys.stdout.write(char)
        sys.stdout.flush()

    print()


def print_banner(banner):
    """Prints a banner

    Displays a passed banner so a user is clear what menu they are viewing.
    """

    print('\n' + f'{Colors.blue}*'*80)
    print(f"\n\t{banner}")
    print('\n' + f'{Colors.blue}*'*80)
    print("")


def click_to_continue():
    """Waits for user to click

    Request a user press enter to continue, used in a few places so
    broken out to a function for consistent display across the app.
    """

    input(f"\n\n\t{Colors.yellow}Press Enter to continue: \n")


def print_selected_menu(heading, menu_options, choice_made=None):
    """Prints a passed menu

    Prints a menu requesting a user to decide whether they
    wish to update the purchases or sales google sheet.
    Reprint the menu if a user doesn't select a valid option

    Returns: choice.
    """
    # pylint: disable-next=global-statement
    global choice
    clear_screen()
    print_banner(heading)

    print("Select")
    print("")
    for k, v in menu_options.items():
        print(f"\t{k: >2} - " + f"{Colors.blue}{v}")
    print("")

    choice = choice_made

    choice = request_input_from_user()

    while choice not in menu_options:
        print(f"{Colors.red}\nYou have selected an option that \
            does not exist, please try again...\n")
        sleep(2)
        print_selected_menu(heading, menu_options, choice_made=None)

    return choice


def show_details_on_vat():
    """Displays VAT info

    Display details on VAT in Ireland.
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

    typewriter_print("\n\tPlease check which tax rate applies \
        if you are unsure\n")
    for k, v in irish_vat_rates.items():
        print("\t" + "*"*72)
        print(f"{Fore.LIGHTWHITE_EX}\t{k}%" + f"{Fore.BLUE}{v}")
        sleep(1.5)

    click_to_continue()


def display_message(message, wait_time=None, is_warning=True):
    """Displays a provided message

    Displays a message passed to the function, if a wait_time is
    passed the message displays for that time, if not a user must
    click to continue.  Is_warning determines the colour of the
    printed message.  Red for warning, green for informative.
    """

    if is_warning:
        print("\n\n\t" + f"{Colors.red}{message}\n")
    else:
        print("\n\n\t" + f"{Colors.green}{message}\n")

    if wait_time:
        sleep(wait_time)
    else:
        click_to_continue()


def display_wait_message(wait_message):
    """Displays a message advising a user of potential delays

    Displays a wait message to keep a user engaged while data is retrieved.
    """

    print(f"{Colors.blue}\n  ,,")
    print(f"{Colors.blue}c(_)'", end=" ")
    typewriter_print(f"{wait_message}...\n\n")


def get_selected_worksheet(sheet):
    """Assigns a 'sheet' variable between purchases and sales

    Returns either purchases/sales worksheet so code is mostly
    reusable for both.
    """

    if sheet == "purchases":
        sheet = PURCHASES_SHEET
    else:
        sheet = SALES_SHEET

    return sheet


def get_current_date_and_time():
    """Retrieves current date & time

    Returns the current date and time (formatted) to accurately
    log a transaction. Format of date is compatible with
    google-sheets (mm/dd/YYYY).
    """

    now = datetime.datetime.now()

    # using (month/day/year) format for better google sheets integraton
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M:%S")
    return (date, time)


def get_month():
    """Retieves current month

    Returns the current month so the correct spreadsheet can be updated.
    """

    now = datetime.datetime.now()

    month = now.strftime("%B")

    return month


def request_input_from_user():
    """Request input from a user

    Ask the user to make a selection, broken out to a function
    for consistent behaviour across the application

    Returns: user_choice in lowercase, and stripped of whitespace.
    """

    typewriter_print("\nChoose an option:\n")
    user_choice = input().lower().strip()

    return user_choice


def request_user_select_a_month(sheet):
    """Request a user select from available months/sheets

    Function to request a user selects a month from available months

    Returns: a tuple of (month, available_months).
    """

    month = input("\nPlease select a month to review " + f"{Colors.green}\
        (Press L to list available months): \n")
    month = month.strip().lower().capitalize()

    available_months = get_list_of_all_sheet_titles(sheet)

    if month.startswith("L"):
        print(available_months)
        month = input("\nPlease make a selection: \n")
        month = month.strip().lower().capitalize()

    if month in available_months:
        display_wait_message("This might take a few seconds")

    return (month, available_months)


def get_length_of_longest_list_item(list_to_check):
    """Finds longest list item

    Returns the longest string in a list of strings,
    useful for formatting output and improving readability.
    """

    return len(sorted(list_to_check, key=len, reverse=True)[0])


def request_new_transaction(sheet, details=None,
                            price_including_vat=None, rate=None):
    """Requests transaction info from a user

    Function to collect the info needed to add a new transaction t
    o a google sheet

    Returns: a tuple of (details, total_price_including_vat, vat_rate).
    """
    # pylint: disable-next=global-statement
    global total_price_including_vat
    # pylint: disable-next=global-statement
    global vat_rate

    clear_screen()
    print_banner(f"Add {sheet}")

    print(f"Please provide details of the new {sheet} transaction here:\n\n")

    # Questions as variables so size can be determined to neatly display output
    details_q = "Details"
    totals_q = "Total including VAT:"
    vat_rate_q = "Which VAT rate applies? (Press Enter for more details)"

    width = get_length_of_longest_list_item([details_q, totals_q, vat_rate_q])

    space = "  \n"
    formatted_details_q = f"{details_q}" + "."*(width - len(details_q)) + space
    formatted_price_q = f"{totals_q}" + "."*(width - len(totals_q)) + space + \
        "€"
    formatted_vat_rate_q = f"{vat_rate_q}" + "."*(width - len(vat_rate_q)) \
        + space

    vat_rate = rate
    total_price_including_vat = price_including_vat

    if details is None:
        details = input(formatted_details_q).strip()
    else:
        print(formatted_details_q + f"{details}")

    if total_price_including_vat is None:
        total_price_including_vat = input(formatted_price_q).strip()

        try:
            total_price_including_vat = float(total_price_including_vat)

        except ValueError:
            display_message("Please check that the total price is a number", 0)
            request_new_transaction(sheet=sheet, details=details)

    else:
        print(formatted_price_q + str(total_price_including_vat))

    if vat_rate is None:
        vat_rate = input(formatted_vat_rate_q).strip()

        if "%" in vat_rate:
            vat_rate = vat_rate.replace("%", "")

        if vat_rate in ["23", "13.5", "9", "4.8", "0"]:
            pass
        elif vat_rate is None or vat_rate == "":
            show_details_on_vat()
            request_new_transaction(
                sheet=sheet,
                details=details,
                price_including_vat=total_price_including_vat
            )
        else:
            display_message("Please check this is a valid tax rate", 2)
            show_details_on_vat()
            request_new_transaction(
                sheet=sheet,
                details=details,
                price_including_vat=total_price_including_vat
            )

    return (details, total_price_including_vat, vat_rate)


def calculate_vat(total_including_vat, rate):
    """Calculate and formats VAT for updating sheets

    Calculate appropriate vat and returns a comma separated string for
    updating the google sheet.
    """

    vat_applicable = round(
        ((float(total_including_vat) * float(rate)) / 100), 2
    )

    # return [vat 23%, vat 13.5%, vat 9%, total vat, exempt]
    if rate == "23":
        return [vat_applicable, 0, 0, vat_applicable, 0]

    elif rate == "13.5":
        return [0, vat_applicable, 0, vat_applicable, 0]

    elif rate == "9":
        return [0, 0, vat_applicable, vat_applicable, 0]

    elif rate == "0":
        return [0, 0, 0, 0, total_including_vat]


def generate_next_invoice_number(sheet):
    """Generates next invoice number based on last used

    Function to get the last available invoice number on a google sheet
    and iterates it by 1.
    """

    ledger = get_selected_worksheet(sheet)

    all_months = get_list_of_all_sheet_titles(sheet)
    all_months = reversed(all_months)

    for month in all_months:
        all_data = ledger.worksheet(month).get_all_values()

        last_row = all_data[-1]

        # subtracting 1 below to account for gspread column v list numbering
        last_invoice_number = last_row[Columns.invoice_number - 1]

        try:
            # pylint: disable-next=using-constant-test
            if str(last_invoice_number).isnumeric:
                # return last invoice number + 1 (next available)
                return int(last_invoice_number) + 1
        except ValueError:
            # using try/except to determine whether values are numeric or
            # not safely. No error reporting is needed here so choosing
            # to pass
            pass


def create_sheet_if_not_available(sheet, dont_provide_option=False):
    """Creates a new sheet if a unavailable

    Function to check if a sheet for a particular month is
    available, and direct a user to create one if necessary.
    Accepting a dont_provide_option to pass through to
    create_new_sheet function and ignoring asking a user which
    month they wish to create a sheet for.
    """

    month = get_month()
    available_months = get_list_of_all_sheet_titles(sheet)

    if month not in available_months:
        display_message(f"No sheet available for {month}", 1)
        create_new_sheet(sheet, dont_provide_option)


def add_new_transaction(sheet):
    """Allows a user add a sales/purchases transaction

    Function to add a new transaction to a worksheet.
    This function checks if a sheet for the current month is available
    & generates it if necessary.
    """

    ledger = get_selected_worksheet(sheet)

    create_sheet_if_not_available(sheet)

    details, total_including_vat, rate = request_new_transaction(sheet=sheet)
    date, _ = get_current_date_and_time()
    invoice_number = generate_next_invoice_number(sheet)
    if invoice_number is None or invoice_number == "":
        invoice_number = input(f"{Colors.red}\n\tNo invoice number available, \
            please manually enter one: {Colors.white}\n")
    formatted_vat_details = calculate_vat(total_including_vat, rate)

    formatted_row = [date, details, invoice_number,
                     total_including_vat] + formatted_vat_details

    try:
        month = get_month()
        ledger.worksheet(month).append_row(formatted_row)
        display_message("Sheet updated successfully", 2, False)

    except FileNotFoundError as e:
        display_message(f"Can't find file: {e}", 3)

    sub_menu(sheet)


def display_all_transactions_for_month(sheet, month=None):
    """Displays all transactions for a particular month

    Function to display google worksheet to the terminal for
    inspection purposes. This function tracks the largest item
    in each column to provide a correctly formatted table.
    """

    ledger = get_selected_worksheet(sheet)
    if month is None:
        create_sheet_if_not_available(sheet, dont_provide_option=True)
        month = get_month()

    num_of_rows = len(ledger.worksheet(month).col_values(1))
    num_of_cols = len(ledger.worksheet(month).row_values(1))

    columns_list = []

    for i in range(num_of_cols):
        new_list = ledger.worksheet(month).col_values(i + 1)
        columns_list.insert(i, new_list)

    print(f"\n{Colors.magenta}{month}")
    print(f"{Colors.blue}-" * 80)

    dont_color = True

    for idx, i in enumerate(range(num_of_rows)):
        # enumerating of rows and only colouring the first row of headings
        # for greater readability
        dont_color = idx >= 1
        for y in range(num_of_cols):
            width = get_length_of_longest_list_item(columns_list[y])
            column_width = width - len(columns_list[y][i])
            if not dont_color:
                print(f"{Colors.blue}{columns_list[y][i]}" + " \
                    "*column_width, end=" | ")

            else:
                print(f"{columns_list[y][i]}" + " "*column_width, end=" | ")
        print()

    click_to_continue()


def get_list_of_all_sheet_titles(sheet):
    """Creates a list of sheet titles/months

    Returns a list of all sheet titles, i.e: available months.
    """

    ledger = get_selected_worksheet(sheet)
    all_sheets = ledger.worksheets()
    months = []

    for sheet in all_sheets:
        months.append(sheet.title)

    return months


def display_all_transactions_for_a_selected_month(sheet):
    """Display all transactions for a provided month

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
        print(f"\nAvailable months: {Colors.green}{months}")
        display_message(
            f"Worksheet not found for chosen month, returning to \
                {sheet} menu!", 3
        )
        clear_screen()
        sub_menu(sheet)


def create_new_sheet(sheet, dont_provide_option=False):
    """Creates a new purchases/sales sheet

    Function to create a new sheet for the current month or a
    given month.
    """

    all_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    month = get_month()
    available_months = get_list_of_all_sheet_titles(sheet)

    if month in available_months:
        display_message("A sheet exists for the current month", 3)
        sub_menu(sheet)

    if sheet == "sales":
        exempt_heading = "Exempt"
    else:
        exempt_heading = "Intra-EU"

    headings = ["Date",	"Details", "Invoice", "Total", "Vat 23%",
                "Vat 13.5%", "VAT 9%", "VAT", f"{exempt_heading}"]

    if not dont_provide_option:
        response = input(
            "\n\tAdd a sheet for the current month? \
                (n to create for another)" + f"{Colors.green} (y/n):  \n"
        )
        response = response.lower().strip()

    else:
        response = "y"

    if response.startswith("y"):
        month = get_month()
        ledger = get_selected_worksheet(sheet)

        try:
            ledger.add_worksheet(month, rows=150, cols=10)
            ledger.worksheet(month).append_row(headings)
            ledger.worksheet(month).format("A1:I1", {'backgroundColor': {
                'blue': 0.65882355,
                'green': 0.84313726,
                'red': 0.7137255
            }})
            display_message(f"Worksheet created for {month}", 2, False)
        except FileExistsError as e:
            print(f"File already exists: \n{e}")

    elif response.startswith("n"):
        months = get_list_of_all_sheet_titles(sheet)
        print(f"\n\t{Colors.green}Already created: \
            " + f"\n\t{Colors.white}{months}\n")
        new_month = input("\n\tWhich month would you like to add?  \n")
        new_month = new_month.strip().lower().capitalize()

        if new_month not in months and new_month in all_months:
            ledger = get_selected_worksheet(sheet)

            try:
                ledger.add_worksheet(new_month, rows=150, cols=10)
                ledger.worksheet(new_month).append_row(headings)
                ledger.worksheet(new_month).format("A1:I1", {
                    'backgroundColor': {
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
    """Displays main menu

    Calls the generic print_selected_menu function with
    main_menu specific options, heading, and handles
    user input.
    """

    heading = "VAT Calculator"
    menu_options = {
        "1": "Sales",
        "2": "Purchases",
        "x": "Exit"
    }

    date, time = get_current_date_and_time()
    print(f"\n{date} - {time}")

    selection = print_selected_menu(heading, menu_options, choice_made=None)

    if selection == "1":
        sub_menu("sales")

    if selection == "2":
        sub_menu("purchases")

    if selection == "x":
        clear_screen()
        print_banner("Goodbye...")
        sleep(2)
        sys.exit(0)


def user_selected_month_from_available_months(sheet):
    """Displays available months and request a user select one

    Function to request a user to select a month from available
    months to review transaction totals.
    """

    available_months = get_list_of_all_sheet_titles(sheet)

    if len(available_months) > 0:
        month = None
        while month not in available_months:
            print(f"\nAvailable months: {Colors.green}{available_months}")
            month = input("\nPlease enter a month from the available options:\
                 \n")
            month = month.strip().lower().capitalize()

        if month in available_months:
            display_wait_message("This might take a few seconds")

        return month

    else:
        display_message("No months a currently available, \
            please add one first", 3)
        totals_menu(sheet)


def calculate_total_of_totals_year_to_date(sheet, run_directly=False):
    """Calculate year-to-date totals for all figures

    Function to calculate sales/puchases, each vat rate, total vat
    and vat exempt totals so a user can get a year to date summary.
    """

    all_months = get_list_of_all_sheet_titles(sheet)

    totals = []
    vat_23 = []
    vat_13_5 = []
    vat_9 = []
    vat_total = []
    exempt_total = []

    choices_dict = {
        "total": totals,
        "vat_23": vat_23,
        "vat_13.5": vat_13_5,
        "vat_9": vat_9,
        "vat_total": vat_total,
        "exempt_total": exempt_total
    }

    if sheet == "sales":
        total_heading = "Sales"
        exempt_heading = "Exempt"

    else:
        total_heading = "Purchases"
        exempt_heading = "Intra-EU"

    headings_dict = {
        "total": total_heading,
        "vat_23": "23% VAT",
        "vat_13.5": "13.5% VAT",
        "vat_9": "9% VAT",
        "vat_total": "VAT",
        "exempt_total": exempt_heading,
    }

    for k, v in choices_dict.items():
        sleep(10)
        for month in all_months:
            sleep(3)
            _, month, rounded_total = get_monthly_total_for(sheet, k, month)
            choices_dict[k].append(rounded_total)

    print(f"\n{Colors.magenta}{sheet.capitalize()} year-to-date totals")
    print(f"{Colors.blue}-" * 80)

    for k, v in choices_dict.items():
        print(f"{Colors.green}{headings_dict[k]:<13}", end="")
    print()

    for k, v in choices_dict.items():
        print(f"{Colors.blue}€{sum(v):<12.2f}", end="")

    print("\n")

    # avoid needing to click to continue twice when this is
    # run as part of totals menu option 7
    if run_directly:
        click_to_continue()


def print_all_monthly_totals_on_individual_lines(sheet):
    """Outputs a stream of all year-to-date monthly totals

    Function to display all monthly totals on their own
    seperate line, and after this output display
    the year to date totals.
    """

    all_months = get_list_of_all_sheet_titles(sheet)

    for month in all_months:
        print_monthly_totals_on_one_line(sheet, month, print_all_months=True)
        # sleep added here to slow down api usage as the program
        # was experiencing
        # -APIError: [429]: Quota exceeded for quota metric 'Read requests'
        #   and limit 'Read requests per minute per user
        sleep(10)

    calculate_total_of_totals_year_to_date(sheet)
    click_to_continue()


def print_monthly_totals_on_one_line(sheet, month=None,
                                     print_all_months=False):
    """Outputs a chosen monthly total

    Function to display a monthly total on it's own
    seperate line.
    """

    choices = ["total", "vat_23", "vat_13.5", "vat_9",
               "vat_total", "exempt_total"]
    messages = []
    months = []
    rounded_totals = []

    if month is None:
        month = user_selected_month_from_available_months(sheet)

    for option in choices:
        message, month, rounded_total = get_monthly_total_for(sheet, option,
                                                              month)
        messages.append(message)
        months.append(month)
        rounded_totals.append(rounded_total)

    print(f"\n{Colors.magenta}{months[0]} totals")
    print(f"{Colors.blue}-" * 80)

    for message in messages:
        print(f"{Colors.green}{message:<13}", end="")
    print()

    for rounded_total in rounded_totals:
        print(f"{Colors.white}€{rounded_total:<12.2f}", end="")

    if not print_all_months:
        print("\n")
        click_to_continue()

    else:
        print()


def get_monthly_total_for(sheet, option, month=None):
    """Calculates a monthly total for a provided column

    Helper function to calculate a monthly total for
    a selected column.
    """

    if option == "total":
        message = sheet.capitalize()
        column = Columns.total

    elif option == "vat_23":
        message = "23% VAT"
        column = Columns.vat_23

    elif option == "vat_13.5":
        message = "13.5% VAT"
        column = Columns.vat_13_5

    elif option == "vat_9":
        message = "9% VAT"
        column = Columns.vat_9

    elif option == "vat_total":
        message = "VAT"
        column = Columns.vat

    elif option == "exempt_total":
        column = Columns.exempt
        if sheet == "sales":
            message = "Exempt"
        else:
            message = "Intra-EU"

    if month is None:
        month = user_selected_month_from_available_months(sheet)

    ledger = get_selected_worksheet(sheet)

    totals_without_header = ledger.worksheet(month).col_values(column)[1:]

    combined_total = sum([float(total) for total in totals_without_header])
    rounded_total = round(float(combined_total), 2)

    return (message, month, rounded_total)


def get_total_for_all_months(column, sheet):
    """Calculates a year-to-date total for a chosen column

    Function that calculates a year-to-date total
    for provided column.
    """

    months = get_list_of_all_sheet_titles(sheet)

    messages = []
    all_months = "'all months'"
    rounded_totals = []

    for month in months:
        message, month, rounded_total = get_monthly_total_for(sheet, column,
                                                              month)
        messages.append(message)
        rounded_totals.append(rounded_total)

    return (messages[0], all_months, sum(rounded_totals))


def totals_menu(sheet):
    """Displays a menu for all totals available purchases/sales

    Calls the generic print selected_menu function with
    totals specific options for a user to interogate the
    data for a given month.
    """

    heading = f"{sheet.capitalize()} totals"
    totals_menu_options = {
        "1": "Month: Display all totals",
        "2": f"Month: {sheet.capitalize()} (including VAT)",
        "3": "Month: VAT (23%)",
        "4": "Month: VAT (13.5%)",
        "5": "Month: VAT (9%)",
        "6": "Month: VAT (combined)",
        "7": f"Month: Tax exempt {sheet}",
        "8": "Year-to-date: Display all totals",
        "9": "Year-to-date: Display totals",
        "10": f"Year-to-date: {sheet.capitalize()} (including VAT)",
        "11": "Year-to-date: VAT (23%)",
        "12": "Year-to-date: VAT (13.5%)",
        "13": "Year-to-date: VAT (9%)",
        "14": "Year-to-date: Total VAT (combined)",
        "15": f"Year-to-date: Tax exempt {sheet}",
        "x": f"Back to {sheet} menu"
    }

    selection = print_selected_menu(
        heading, totals_menu_options, choice_made=None)

    if selection == "1":
        print_monthly_totals_on_one_line(sheet)
        totals_menu(sheet)

    if selection == "2":
        message, month, rounded_total = get_monthly_total_for(sheet, "total")
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "3":
        message, month, rounded_total = get_monthly_total_for(sheet, "vat_23")
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "4":
        message, month, rounded_total = get_monthly_total_for(sheet,
                                                              "vat_13.5")
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "5":
        message, month, rounded_total = get_monthly_total_for(sheet, "vat_9")
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "6":
        message, month, rounded_total = get_monthly_total_for(sheet,
                                                              "vat_total")
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "7":
        message, month, rounded_total = get_monthly_total_for(sheet,
                                                              "exempt_total")
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "8":
        display_wait_message("This will take a few minutes")
        print_all_monthly_totals_on_individual_lines(sheet)
        totals_menu(sheet)

    if selection == "9":
        display_wait_message("This will take a few minutes")
        calculate_total_of_totals_year_to_date(sheet, run_directly=True)
        totals_menu(sheet)

    if selection == "10":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("total",
                                                                 sheet)
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "11":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months("vat_23",
                                                                 sheet)
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "12":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months(
            "vat_13.5", sheet)
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "13":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months(
            "vat_9", sheet)
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "14":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months(
            "vat_total", sheet)
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "15":
        display_wait_message("This might take a few seconds")
        message, month, rounded_total = get_total_for_all_months(
            "exempt_total", sheet)
        display_message(
            f"{message} for {month}: {Colors.white}€{rounded_total:.2f}",
            is_warning=False
        )
        totals_menu(sheet)

    if selection == "x":
        sub_menu(sheet)


def sub_menu(sheet):
    """Prints either sales/purchases menu based on selected sheet

    Calls the generic print_selected_menu function with
    sub_menu specific options, heading, and handles
    user input.
    """

    menu_options = {
        "1": "Add a new transaction",
        "2": "Display all transactions for the current month",
        "3": "Display all transactions for a given month",
        "4": f"Create a {sheet} sheet for current month (if none yet exists)",
        "5": "Show details on local VAT rates",
        "6": "Display 'Totals' menu",
        "x": "Return to main menu"
    }

    selection = print_selected_menu(sheet.capitalize(), menu_options,
                                    choice_made=None)

    if selection == "1":
        add_new_transaction(sheet)
    if selection == "2":
        display_wait_message("This might take a few seconds")
        display_all_transactions_for_month(sheet)
        sub_menu(sheet)
    if selection == "3":
        display_all_transactions_for_a_selected_month(sheet)
        sub_menu(sheet)
    if selection == "4":
        create_new_sheet(sheet)
        sub_menu(sheet)
    if selection == "5":
        show_details_on_vat()
        sub_menu(sheet)
    if selection == "6":
        totals_menu(sheet)

    if selection == "x":
        main_menu()


def main():
    """main

    main function.
    """

    try:
        main_menu()
    except RuntimeError:
        print("Something went wrong, try rebooting")


if __name__ == "__main__":
    main()
