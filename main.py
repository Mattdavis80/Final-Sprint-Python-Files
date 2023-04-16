# Semester 1 - Final Sprint Week - Simpson Carpet World Python Program
# Group 3 - Michael Bennett, Matt Davis, Evan Holloway, Kostiantyn Karzhanov, Daniel Shepelev, Michael Sheridan
# Last Modified - April 13th, 2023

# Import Statements
import re
import datetime
import FormatValues as FV
import time

# Variables for Today
today = datetime.datetime.now()
today_str = datetime.datetime.strftime(today, "%d-%m-%Y")

# Assign required constants
DATE_COMMISSION_CALC = 1
DATE_START_COMPANY = datetime.datetime(2000, 1, 1)
THRESHOLD_EMP_AGE = 100
DATE_THRESHOLD_EMP_AGE = today - datetime.timedelta(THRESHOLD_EMP_AGE * 365.25)

# - lists for validation and receipts
VALID_PROV = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
BRANCH_LIST = ["St. John's", "Mt. Pearl", "Carbonear", "Northern Bay"]

# - constants for output structure
HEADER_COMPANY_NAME = "Simpson Carpet World"
SUBHEADER = "Company Services System"
LINES_HEADER = "<>" * 13
LINES_NOTE = "-" * 121

# Read data from the file defaults.dat
f = open('defaults.dat', 'r')
employee_num = int(f.readline())
inventory_num = int(f.readline())
commission_rate = float(f.readline())
bonus_threshold = int(f.readline())
commission_bonus_amt = int(f.readline())
reorder_num = int(f.readline())
customer_num = int(f.readline())
order_num = int(f.readline())
HST = float(f.readline())
f.close()

# A number of lists that will help with validating input in option_four() function
item_numbers_list = []
item_descriptions_list = []
emp_numbers_list = []
customer_numbers_list = []

# Read required data from the inventory file
f = open('inventoryLog.dat', 'r')
for item_data_line in f:
    item_line = item_data_line.split(',')
    item_number = int(item_line[0].strip())
    item_description = item_line[1].strip()
    retail_price = item_line[7].strip()

    item_numbers_list.append(item_number)
    item_descriptions_list.append(item_description)
f.close()

# Read required data from employee file
f = open("employeeLog.dat", "r")
for employee_data_line in f:
    employee_line = employee_data_line.split(',')
    employee_number = int(employee_line[0].strip())

    emp_numbers_list.append(employee_number)
f.close()

# Read required data from customer file
f = open("customerLog.dat", "r")
for customer_data_line in f:
    customer_line = customer_data_line.split(',')
    customer_number = int(customer_line[0].strip())

    customer_numbers_list.append(customer_number)
f.close()


# ---------------------------------
# Validation functions starts here
# ---------------------------------

def check_char_num(value_name, value_to_check, high_char_num, low_char_num=1):
    # The function checks whether the length of the given value ("value_to_check") is within the specified range or returns "None"
    if value_to_check == "":
        # if "value_to_check" is an empty string show the warning message
        print(f"\nSorry the \"{value_name}\" cannot be empty")
    elif low_char_num <= len(value_to_check) <= high_char_num:
        # if the length is within the specified range return the value
        return value_to_check
    else:
        # if the length is NOT within the specified range, show a warning message
        if low_char_num == high_char_num:
            print(
                f"\nSorry, the \"{value_name}\" must be \"{high_char_num}\" characters long. You entered \"{len(value_to_check)}\"")
        else:
            print(
                f"\nSorry, the \"{value_name}\" must be from \"{low_char_num}\" to \"{high_char_num}\" characters long. You entered \"{len(value_to_check)}\"")


def get_accepted_set(format=False):
    # The function returns a certain set of accepted characters depending on the "format" given
    if not format or format == "A-z'- .#0-9":
        return set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'- .#0123456789")
    elif format == "A-z'- .":
        return set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'- .")
    elif format == "A-z'-":
        return set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'-")
    else:
        return set(format)


def check_valid_format(value_name, value_to_check, format=False):
    # The function checks if the given value ("value_to_check") is valid based on the specified "format"

    # "get_accepted_set" returns a certain set of accepted characters depending on the specified "format"
    accepted_char = get_accepted_set(format)

    if set(value_to_check).issubset(accepted_char):
        # If "value_to_check" has a valid format return this value
        return value_to_check
    else:
        # Show the warning message if not
        print(f"\nSorry, the \"{value_name}\" is not valid. You entered: \"{value_to_check}\"")


def get_valid_date(value_name, date_threshold_low, date_threshold_high, format="%d-%m-%Y", format_descr="DD-MM-YYYY"):
    # Prompt the user to input the "date" in the given format (default is "DD-MM-YYYY")
    date_input = input(f"Please enter {value_name} as {format_descr}: ")

    try:
        # Attempt to convert the input string to a datetime object
        date_checked = datetime.datetime.strptime(date_input, format)
    except:
        # If the conversion fails, display an error message
        if date_input == "":
            print(f"\nSorry the \"{value_name}\" cannot be empty")
        else:
            print(f"\nSorry, the \"{value_name}\" is not valid. You entered: \"{date_input}\"")
    else:
        # Check if the date is within valid bounds. Return "date_input" if it is valid or show a message and return "None"
        if date_threshold_low <= date_checked <= date_threshold_high:
            return date_input
        elif date_checked < date_threshold_low:
            # If the date is earlier than the minimum allowed date, show a message with the closest valid date
            print(
                f"\nSorry, the \"{value_name}\" is not valid. The closest valid date is: {date_threshold_low.strftime(format)}")
        elif date_checked > date_threshold_high:
            # If the date exceeds the upper limit, show an error message.
            print(f"\nSorry, the \"{value_name}\" is not valid. You entered: \"{date_input}\"")


# ----------------------------
# The end of validation block
# ----------------------------

def back_main_menu(key_name="Return"):
# The function provides a convenient way for users to return to the main menu of a program 
    return input(f"\nHit \"{key_name}\" to go back to the Main Menu: ")


def show_title(symbols_up_n_down, title, add_symb_num = 2):
# The function shows the title surrounded by specified "symbols_up_n_down". Returns "None"
    align_num_chars = len(title) + add_symb_num

    print()
    print(f"{symbols_up_n_down}" * align_num_chars)
    print(f"{title :^{align_num_chars}}")
    print(f"{symbols_up_n_down}" * align_num_chars)
    print()


def option_one():
    """A function that will enter a new employee's information, then
    append it all into the employee file as a new record."""

    global employee_num

    while True:
        employee_info = []

        # First Name, mandatory input, converted to Title-case
        while True:
            # Repeat the loop until the user enters a valid "first name"
            emp_f_name = input("First Name: ")
            # Check if the length of "emp_f_name" is within the specified range (1-15) or return "None"
            emp_f_name = check_char_num("first name", emp_f_name, 15)

            if emp_f_name:
                # Check if "emp_f_name" is valid based on the "format" given ("A-z'-")
                emp_f_name = check_valid_format("first name", emp_f_name, "A-z'-")

                if emp_f_name:
                    # If "emp_f_name" is valid make it "Title Case" and exit the loop
                    emp_f_name = emp_f_name.title()
                    break

            # Show a message and repeat the loop
            print("Please try again\n")

        # Last Name, mandatory input, converted to Title-case
        while True:
            # Repeat the loop until the user enters a valid "last name"
            emp_l_name = input("Last Name: ")
            # Check if the length of "emp_l_name" is within the specified range (1-15) or return "None"
            emp_l_name = check_char_num("last name", emp_l_name, 15)

            if emp_l_name:
                # Check if "emp_l_name" is valid based on the "format" given ("A-z'-")
                emp_l_name = check_valid_format("last name", emp_l_name, "A-z'-")

                if emp_l_name:
                    # If "emp_l_name" is valid make it "Title Case" and exit the loop
                    emp_l_name = emp_l_name.title()
                    break

            # Show a message and repeat the loop
            print("Please try again\n")

        # Street Address, mandatory input, converted to Title-case
        while True:
            # Repeat the loop until the user enters a valid "street address"
            str_add = input("Street Address: ")
            # Check if the length of "str_add" is within the specified range (1-30) or return "None"
            str_add = check_char_num("street address", str_add, 30)

            if str_add:
                # Check if "str_add" is valid based on the "format" given ("A-z'- .#0-9")
                str_add = check_valid_format("street address", str_add, "A-z'- .#0-9")

                if str_add:
                    # If "str_add" is valid make it "Title Case" and exit the loop
                    str_add = str_add.title()
                    break

            # Show a message and repeat the loop
            print("Please try again\n")

        # City, mandatory input, converted to Title-case
        while True:
            # Repeat the loop until the user enters a valid "city"
            city = input("City: ")
            # Check if the length of "city" is within the specified range (1-19) or return "None"
            city = check_char_num("city", city, 19)

            if city:
                # Check if "city" is valid based on the "format" given ("A-z'- .")
                city = check_valid_format("city", city, "A-z'- .")

                if city:
                    # If "city" is valid make it "Title Case" and exit the loop
                    city = city[:-1].title() + city[-1].lower()
                    break

            # Show a message and repeat the loop
            print("Please try again\n")

        # Province, mandatory input,converted to Upper-case, compared to valid list of provinces
        while True:
            prov = input(f"Province ({', '.join(VALID_PROV)}): ").upper()

            if prov == "":
                print("Province field cannot be empty, Please re-enter")
            elif len(prov) != 2:
                print("Please re-enter province as (XX)")
            elif prov not in VALID_PROV:
                print("Please enter a valid province")
            else:
                break

        # Postal Code, mandatory input, must be valid format as X0X0X0, X0X 0X0 or X0X-0X0
        # The pattern below is used to compare against user input, this will be done using Regular Expressions
        pattern = r"^[A-Z]\d[A-Z][ -]?\d[A-Z]\d$"

        while True:
            # Repeat the loop until the user enters a valid "Postal code"
            # Prompt the user to input a postal code
            post_code = input("Postal Code: (e.g. A1A 1A1): ").upper()

            if re.match(pattern, post_code):
                # If the input matches the regular expression pattern, format it as "A1A 1A1" and break out of the loop
                post_code = "{0} {1}".format(post_code[:3], post_code[-3:])
                break
            else:
                # If the input does not match the pattern, display an error message and repeat the loop
                print("Invalid postal code. Please re-enter")

        # Phone Number, mandatory input, 10 characters long
        while True:
            # Repeat the loop until the user enters a valid "Phone number"
            # Prompt the user to input a "phone number"
            phone_num = input("Phone number (10 digits): ")

            # Define a regular expression pattern to match any parentheses, dashes, spaces, or slashes in the input
            regex_object = re.compile(r"[() -/]")
            # Replace any matched characters from the input with the empty string using the regular expression pattern
            phone_num = regex_object.sub("", phone_num)

            if phone_num == "":
                # If the phone number is empty, display an error message and repeat the loop
                print("Phone number cannot be empty, Please re-enter")
            elif len(phone_num) != 10:
                # If the phone number is not 10 digits long, display an error message and repeat the loop
                print("Please enter phone number as 10 digits")
            elif not phone_num.isdigit():
                # If the phone number contains non-digit characters, display an error message and repeat the loop
                print("Please enter a valid phone number")
            else:
                # If the phone number is valid, format it as ###-###-#### and break out of the loop
                phone_num = phone_num[:3] + "-" + phone_num[3:6] + "-" + phone_num[6:]
                break

                # Date hired, mandatory input, valid date
        while True:
            # Repeat the loop until the user enters a valid "Date hired"
            # Prompt the user to input the "Date hired"
            date_hired = get_valid_date("date hired", DATE_START_COMPANY, today)

            if date_hired:
                # If the "date hired" is valid exit the loop
                break

            # Show a message and repeat the loop
            print("Please try again\n")

        # Employee Branch Number, mandatory input
        while True:
            try:
                emp_branch_num = int(input("Last digit of Branch Number: NL-00X (0-3): "))
            except ValueError:
                print("Please enter valid number")
            else:
                if emp_branch_num < 0 or emp_branch_num > 3:
                    print("Please enter a valid branch number")
                else:
                    break

        # Employee title, mandatory input, checked via regular expressions, Alpha only 20 character max size.
        pattern = r"^[a-zA-Z ]{0,20}$"
        while True:
            emp_title = input("Employee Title: ").title()
            if re.match(pattern, emp_title):
                break
            else:
                print("Invalid Title, Please re-enter")

        # Employee Salary, mandatory input
        while True:
            try:
                emp_salary = float(input("Employee Salary: "))
            except ValueError:
                print("Please enter a valid number")
            else:
                emp_salary = round(emp_salary, 2)

                if emp_salary < 13000:
                    print("This salary is below minimum wage, please re-enter")
                elif emp_salary > 100000:
                    print("This salary is above the highest paid person at Sampson's Carpet, Please re-enter")
                else:
                    break

        # Employee Skills, mandatory input
        while True:
            # Repeat the loop until the user enters a valid "employee skill"
            emp_skills = input("Employee skill: ")
            # Check if the length of "emp_skills" is within the specified range (1-40) or return "None"
            emp_skills = check_char_num("employee skill", emp_skills, 40)

            if emp_skills:
                # Check if "emp_skills" is valid based on the "format" given ("A-z'- .")
                emp_skills = check_valid_format("employee skill", emp_skills, "A-z'- .")

                if emp_skills:
                    # If "emp_skills" is valid make it "Title Case" and exit the loop
                    emp_skills = emp_skills.title()
                    break

            # Show a message and repeat the loop
            print("Please try again\n")

        # Birthdate, mandatory input, valid date
        while True:
            # Repeat the loop until the user enters a valid "Birthdate"
            # Prompt the user to input the "birthdate"
            birthdate = get_valid_date("birthdate", DATE_THRESHOLD_EMP_AGE, today)

            if birthdate:
                # If the "birthdate" is valid exit the loop
                break

            # Show a message and repeat the loop
            print("Please try again\n")

        # Format currency related variables
        emp_salary_out = "{:.2f}".format(emp_salary)

        # Append the new employee information to the "employee_info" list
        employee_info.extend(
            [employee_num, emp_f_name, emp_l_name, str_add, city, prov, post_code, phone_num, date_hired,
             emp_branch_num, emp_title, emp_salary_out, emp_skills, birthdate])

        # Append info to Employee Log data file
        with open('employeeLog.dat', 'a') as fhandle:
            fhandle.write(", ".join(map(str, employee_info)) + "\n")

        # Simulate a loading process
        print()
        print("Adding Employee to System, please wait")
        loading_text = "...."

        for char in loading_text:
            print(char, end="", flush=True)
            time.sleep(0.5)

        print(f" Employee (\"{employee_num}\") successfully added")
        time.sleep(1)

        # Increment employee_num and add all info to employee info list
        employee_num += 1

        # Updating defaults file to new Employee Number
        f = open("defaults.dat", 'w')
        f.write("{}\n".format(str(employee_num)))
        f.write("{}\n".format(str(inventory_num)))
        f.write("{}\n".format(str(commission_rate)))
        f.write("{}\n".format(str(bonus_threshold)))
        f.write("{}\n".format(str(commission_bonus_amt)))
        f.write("{}\n".format(str(reorder_num)))
        f.write("{}\n".format(str(customer_num)))
        f.write("{}\n".format(str(order_num)))
        f.write("{}\n".format(str(HST)))
        f.close()

        while True:
            add_more_emp = input("Would you like to add another employee (Y/N): ").upper()
            if add_more_emp == "Y":
                break
            elif add_more_emp == "N":
                return
            else:
                print("Please Select (Y) for yes or (N) for no")


def option_two():
    pass


def option_three():
    pass


def option_four():
    """A function that is used to enter information for each new customer
       purchase, then append all the info into the customer purchase file
       as a new record."""

    global order_num

    while True:
        purchase_info = []

        print("Enter new order information")
        while True:
            try:
                emp_number = int(input(f"Employee Number ({', '.join(map(str, emp_numbers_list))}): "))
            except ValueError:
                print("Please enter a valid number")
            else:
                if emp_number not in emp_numbers_list:
                    print("Does not match any current employee number - please try again.")
                else:
                    break

        while True:
            try:
                cust_num = int(input(f"Customer ID Number ({', '.join(map(str, customer_numbers_list))}): "))
            except ValueError:
                print("Invalid input - must be an integer.")
            else:
                if cust_num not in customer_numbers_list:
                    print("Invalid customer number - please try again.")
                else:
                    break

        while True:
            try:
                item_num = int(input(f"Item Number ({', '.join(map(str, item_numbers_list))}): "))
            except ValueError:
                print("Invalid input - must be an integer.")
            else:
                if item_num not in item_numbers_list:
                    print("That item number does not match any of our items - please try again.")
                else:
                    break

        while True:
            try:
                quantity = int(input("Enter the quantity purchased: "))
            except ValueError:
                print("Invalid number - please try again")
            else:
                if quantity < 1:
                    print("Invalid quantity - please try again")
                else:
                    break

        with open('inventoryLog.dat', 'r') as fhandle:
            # Read all lines from the inventory file
            lines = fhandle.readlines()

            for record in lines:
                # Loop through the lines in "inventoryLog.dat" until you find the record with the specified item number
                # Remove any trailing whitespace characters
                record = record.rstrip()

                # Check if the record starts with the specified item number
                if record.startswith(str(item_num)):
                    # Split the record into a list of items
                    list_record = [item.lstrip() for item in record.split(',')]
                    # Extract required data and assign it to the variables
                    description = list_record[1]
                    retail_cost = float(list_record[7])

                    # Exit the loop as soon as the required record is found
                    break

        # Calculations for customer purchase
        subtotal = retail_cost * quantity
        HST_amount = subtotal * HST
        order_total = subtotal + HST_amount
        order_date = today_str

        # Format currency related variables
        subtotal_out = "{:.2f}".format(subtotal)
        retail_cost_out = "{:.2f}".format(retail_cost)
        order_total_out = "{:.2f}".format(order_total)

        # Append the new purchase information to the "purchase_info" list
        purchase_info.extend(
            [order_num, order_date, cust_num, item_num, description, retail_cost_out, quantity, subtotal_out,
             order_total_out, emp_number])

        # Open file and write back all data
        with open("customerPurchase.dat", "a") as fhandle:
            # Write the new purchase information to the file as a comma-separated string
            fhandle.write(", ".join(map(str, purchase_info)) + "\n")

        # Simulate a loading process
        print()
        print("Adding Order to System, please wait")
        loading_text = "...."

        for char in loading_text:
            print(char, end="", flush=True)
            time.sleep(0.5)

        print(f" Order (\"{order_num}\") successfully added")
        time.sleep(1)

        # Increment Order Number "order_num"
        order_num += 1

        # Updating defaults file to new Order Number
        with open("defaults.dat", 'w') as fhandle:
            fhandle.write("{}\n".format(employee_num))
            fhandle.write("{}\n".format(inventory_num))
            fhandle.write("{}\n".format(commission_rate))
            fhandle.write("{}\n".format(bonus_threshold))
            fhandle.write("{}\n".format(commission_bonus_amt))
            fhandle.write("{}\n".format(reorder_num))
            fhandle.write("{}\n".format(customer_num))
            fhandle.write("{}\n".format(order_num))
            fhandle.write("{}\n".format(HST))

        while True:
            add_more_order = input("Would you like to add another order (Y/N): ").upper()
            if add_more_order == "Y":
                break
            elif add_more_order == "N":
                return
            else:
                print("Please Select (Y) for yes or (N) for no")


def option_five():
    """A function that is used to process and print out an employee listing."""

    # Print the headings
    print(HEADER_COMPANY_NAME)
    print(f"Employee Listing as of {today_str}")
    print("------------------------------------------------------------------------------")
    print("Employee #    Employee Name          Title               Branch        Salary")
    print("------------------------------------------------------------------------------")

    # Initialize accumulators
    total_employees_acc = 0
    average_salary = 0
    total_salary_acc = 0

    # Open the file to report on
    f = open("employeeLog.dat", "r")
    for emp_data_line in f:
        emp_line = emp_data_line.split(",")

        # Grab values from the file needed for the listing and assign them to variables
        employee_number = int(emp_line[0].strip())
        emp_first_name = emp_line[1].strip()
        emp_last_name = emp_line[2].strip()
        emp_branch = emp_line[9].strip()
        emp_title = emp_line[10].strip()
        emp_salary = float(emp_line[11].strip())
        full_name = emp_first_name + " " + emp_last_name

        # Print the detail lines
        print(
            f"{employee_number}          {full_name:<20s}   {emp_title:<16s}    {emp_branch:>6s}     "f"{FV.FDollar2(emp_salary):>10s}")

        # Update accumulators
        total_employees_acc += 1
        total_salary_acc += emp_salary
        average_salary = total_salary_acc / total_employees_acc

    # Close the file and print the summary data
    f.close()
    print("------------------------------------------------------------------------------")
    print(f"Total Employees: {total_employees_acc:>3d}    Average Salary: {FV.FDollar2(average_salary):>10s}   "
          f"Total Salary: {FV.FDollar2(total_salary_acc):>11s}")


def option_six():
    pass


def option_seven():
    pass


def option_eight():
    """A function that is used to process and print out a reorder listing."""

    # Print the headings
    print(HEADER_COMPANY_NAME)
    print(f"Product Reorder Listing as of {today_str}")
    print("------------------------------------------------------------------------------")
    print("  Item #     Item Name        On Hand     Amt Ordered     Expected After Order")
    print("------------------------------------------------------------------------------")

    # Initialize counters and accumulators
    item_count = 0
    order_amt = 0

    # Open the file to report on
    f = open('inventoryLog.dat', 'r')

    # Loop through each line in the file and process the items
    for item_data_line in f:
        item_line = item_data_line.split(',')
        item_num = int(item_line[0].strip())
        item_description = item_line[1].strip()
        retail_price = float(item_line[7].strip())
        QOH = int(item_line[8].strip())
        reorder_point = int(item_line[9].strip())
        max_amt = int(item_line[10].strip())

        # Set up the condition for the exception in an if statement
        # Check to see if the item needs to be reordered and calculate the amount to order
        while True:
            if QOH <= reorder_point:
                amt_need = max_amt - QOH
                order_amt += (retail_price * amt_need)

                # Print the detail line (items that need to be reordered)
                print(
                    f'  {item_num:>4d}      {item_description:<14s}     {QOH:>4d}     {amt_need:>9d}   {max_amt:>15d}')

                # Update counters and accumulators
                QOH += amt_need
                item_count += 1

            # If the quantity on hand is equal to the max amount, stop processing the item
            elif QOH == max_amt:
                break
            break

    # Close the file and print the summary data
    f.close()
    print("------------------------------------------------------------------------------")
    print(f"Total Items: {item_count:>2d}        Last Order: $30,000.00        Current Order: {FV.FDollar2(order_amt)}")


def problem_solving():
    # read the customer purchase data from the file
    with open('CustomerPurchase.dat', 'r') as f:
        purchases = [line.strip().split(', ') for line in f.readlines()]

    # calculate the sales totals for each employee
    sales_totals = {}

    for purchase in purchases:
        emp_id = purchase[9]
        subtotal = float(purchase[7])

        if emp_id not in sales_totals:
            sales_totals[emp_id] = subtotal
        else:
            sales_totals[emp_id] += subtotal

    # Assign the list of unique employee IDs by extracting them from the dictionary keys and sorting them in ascending order. 
    unique_emp_ids = sorted(sales_totals.keys())

    # Generate output for the user
    print(HEADER_COMPANY_NAME)
    print(f"Commission totals for \"{len(unique_emp_ids)}\" employees as of \"{today.day:02d}-{today.month:02d}-{today.year}\"")
    print("-" * 26)
    print(" Employee #    Commission ")
    print("-" * 26)

    # Calculate the commission for each employee
    for emp_id in unique_emp_ids:
        sales_total = sales_totals[emp_id]
        commission = 0.06 * sales_total

        if sales_total > 5000:
            commission += 200

        # Display the results
        print(f"  {emp_id :<4s}         {FV.FDollar2(commission) :>9s}")

    print("-" * 26)

while True:
    print()
    print(f"{LINES_HEADER :<{len(LINES_HEADER)}}")
    print(f"{HEADER_COMPANY_NAME :^{len(LINES_HEADER)}}")
    print(f"{SUBHEADER :^{len(LINES_HEADER)}}")
    print(f"{LINES_HEADER :<{len(LINES_HEADER)}}")
    print()
    print('1. Enter a New Employee (+)')
    print('2. Enter a New Customer (-)')
    print('3. Enter a New Inventory Item (-)')
    print()
    print('4. Record Customer Purchase (+)')
    print()
    print('5. Print Employee Listing (+)')
    print('6. Print Customers By Branch (-)')
    print('7. Print Orders By Customer (-)')
    print('8. Print Recorder Listing (+)')
    print('9. Print total commission of each employee (Extra) (+)')
    print()
    print('10. Exit Menu')
    print()

    if today.day == DATE_COMMISSION_CALC:
        problem_solving()
    else:
        print(LINES_NOTE)
        print(f" Note: The system performs commission calculations automatically once a month, specifically on the \"{DATE_COMMISSION_CALC}\" of each month")
        print("       If you need to view calculations for today's date, you can access them by selecting the ninth option in the menu")
        print(LINES_NOTE)
    print()

    while True:
        try:
            choice = int(input("Please make a list selection: "))
        except ValueError:
            print("Please enter a valid number")
        else:
            if choice < 1 or choice > 10:
                print("Please enter a number from 1-10 to make a selection")
            else:
                break

    if choice == 1:
        show_title("*", "(1) - Enter a New Employee", add_symb_num = 2)
        print('Welcome to the Employee Portal')
        print("Please enter the following information:")
        print()
        option_one()
    elif choice == 2:
        print()
        print('Second option')
        print("-------------")
        option_two()
    elif choice == 3:
        print()
        print('Third option')
        print("------------")
        option_three()
    elif choice == 4:
        show_title("*", "(4) - Record Customer Purchase", add_symb_num = 2)
        option_four()
    elif choice == 5:
        show_title("*", "(5) - Employee Listing", add_symb_num = 2)
        option_five()
        back_main_menu()
    elif choice == 6:
        print()
        print('Sixth option')
        print("-------------")
        option_six()
    elif choice == 7:
        print()
        print('Seventh option')
        print("--------------")
        option_seven()
    elif choice == 8:
        show_title("*", "(8) - Recorder Listing", add_symb_num = 2)
        option_eight()
        back_main_menu()
    elif choice == 9:
        show_title("*", "(9) - Total commission of each employee", add_symb_num = 2)
        problem_solving()
        back_main_menu()
    elif choice == 10:
        show_title("*", "(10) - Congrats, you have successfully left the program. Hope to see you soon!", add_symb_num = 2)
        exit()