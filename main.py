# Semester 1 - Final Sprint Week - Simpson Carpet World Python Program
# Group 3 - Michael Bennett, Matt Davis, Evan Holloway, Kostiantyn Karzhanov, Daniel Shepelev, Michael Sheridan
# Last Modified - April 6th, 2023

# Import Statements
import re
import datetime
import FormatValues as FV
import time

# Variables for Today
today = datetime.datetime.now()
today_str = datetime.datetime.strftime(today, "%d-%m-%Y")

# Lists for validation and receipts
valid_prov = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
branch_list = ["St. John's", "Mt. Pearl", "Carbonear", "Northern Bay"]

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
    employee_num = int(employee_line[0].strip())

    emp_numbers_list.append(employee_num)
f.close()


# Read required data from customer file
f = open("customerLog.dat", "r")
for customer_data_line in f:
    customer_line = customer_data_line.split(',')
    customer_number = int(customer_line[0].strip())

    customer_numbers_list.append(customer_number)
f.close()

# Read required data from purchases file
f = open("customerPurchase.dat", "r")

for purchase_data_line in f:
    purchase_line = purchase_data_line.split(',')
    order_number = int(purchase_line[0].strip())
f.close()


# -----------------
# Validation start
# -----------------

def check_char_num(value_name, value_to_check, high_char_num, low_char_num = 1):
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
            print(f"\nSorry, the \"{value_name}\" must be \"{high_char_num}\" characters long. You entered \"{len(value_to_check)}\"")
        else:
            print(f"\nSorry, the \"{value_name}\" must be from \"{low_char_num}\" to \"{high_char_num}\" characters long. You entered \"{len(value_to_check)}\"")


def get_accepted_set(format = False):
# The function returns a certain set of accepted characters depending on the "format" given
    if not format or format == "A-z'- .#0-9":
        return set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'- .#0123456789")
    elif format == "A-z'- .":
        return set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'- .")
    elif format == "A-z'-":
        return set("ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'-")
    else:
        return set(format)


def check_valid_format(value_name, value_to_check, format = False):
    # The function checks if the given value ("value_to_check") is valid based on the specified "format"

    # "get_accepted_set" returns a certain set of accepted characters depending on the specified "format"
    accepted_char = get_accepted_set(format)

    if set(value_to_check).issubset(accepted_char):
    # If "value_to_check" has a valid format return this value
        return value_to_check 
    else:
    # Show the warning message if not
        print(f"\nSorry, the \"{value_name}\" is not valid. You entered: \"{value_to_check}\"")

# -----------------
# Validation end
# -----------------


def option_one():
    """A function that will enter a new employee's information, then
    append it all into the employee file as a new record."""

    while True:
        global employee_num
        employee_info = []

        # User Validated Inputs

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
            prov = input("Province (XX): ").upper()

            if prov == "":
                print("Province field cannot be empty, Please re-enter")
            elif len(prov) != 2:
                print("Please re-enter province as (XX)")
            elif prov not in valid_prov:
                print("Please enter a valid province")
            else:
                break

        # Postal Code, mandatory input, must be valid format as X0X 0X0
        # The pattern below is used to compare against user input, this will be done using Regular Expressions
        # The pattern will accept a space or dash between postal code
        pattern = r"^[A-Z]\d[A-Z][ -]?\d[A-Z]\d$"

        while True:
            post_code = input("Postal Code: (e.g. A1A 1A1): ").upper()
            if re.match(pattern, post_code):
                break
            else:
                print("Invalid postal code. Please re-enter")

        # Phone Number, mandatory input, 10 characters long
        while True:
            phone_num = input("Phone number (Without Spaces): ")
            phone_num = phone_num.replace("-", "")
            phone_num = phone_num.replace("/", "")
            if len(phone_num) != 10:
                print("Please format phone number as 10 digits without spaces")
            elif not phone_num.isdigit():
                print("Please enter a valid phone number")
            else:
                phone_num = phone_num[:3] + "-" + phone_num[3:6] + "-" + phone_num[6:]
                break

        # Date hired, mandatory input, valid date
        while True:
            try:
                date_hired = input("Please enter date hired as dd-mm-yyyy: ")
                date_hired = datetime.datetime.strptime(date_hired, "%d-%m-%Y")
            except:
                print("Please enter a valid date: ")
            else:
                date_hired = datetime.datetime.strftime(date_hired, "%d-%m-%Y")
                break

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
                emp_salary = int(input("Employee Salary: "))
            except ValueError:
                print("Please enter a valid number")
            else:
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
            try:
                birthdate = input("Please enter birthdate as dd-mm-yyyy: ")
                birthdate = datetime.datetime.strptime(birthdate, "%d-%m-%Y")
            except:
                print("Please enter a valid date: ")
            else:
                birthdate = datetime.datetime.strftime(birthdate, "%d-%m-%Y")
                break

        # Increment employee_num and add all info to employee info list
        employee_num += 1
        employee_info.append((employee_num, emp_f_name, emp_l_name, str_add, city, prov, post_code, phone_num, date_hired,
                            emp_branch_num, emp_title, emp_salary, emp_skills, birthdate))

        # Append info to Employee Log data file
        f = open('employeeLog.dat', 'a')
        for data in employee_info:
            f.write(", ".join(map(str, data)) + "\n")
        f.close()

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


        # Loading text for recept generation
        print()
        print("Adding Employee to System, please wait")
        loading_text = "...."

        for char in loading_text:
            print(char, end="", flush=True)
            time.sleep(0.5)
        print(f" Employee {employee_num} successfully added. ")
        time.sleep(1)

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

    global order_number
    purchase_info = []

    print("Enter new order information")
    while True:
        try:
            emp_number = int(input("Employee Number: "))
        except ValueError:
            print("Please enter a valid number")
        else:
            if emp_number not in emp_numbers_list:
                print("Does not match any current employee number - please try again.")
                print(f"Employee numbers: {emp_numbers_list}")
            else:
                break

    while True:
        try:
            cust_num = int(input("Customer ID Number: "))
        except ValueError:
            print("Invalid input - must be an integer.")
        else:
            if cust_num not in customer_numbers_list:
                print("Invalid customer number - please try again.")
                print(f"Customer Numbers: {customer_numbers_list}")
            else:
                break

    while True:
        try:
            item_num = int(input("Item Number: "))
        except ValueError:
            print("Invalid input - must be an integer.")
        else:
            if item_num not in item_numbers_list:
                print("That item number does not match any of our items - please try again.")
                print(f"Item Numbers: {item_numbers_list}")
            else:
                break

    while True:
        description = input("Item Description: ").title()
        if description == "":
            print("Cannot be blank - please try again.")
        elif description not in item_descriptions_list:
            print("We do not sell any items of that description - please try again.")
            print(f"Item Descriptions: 'Wool Carpet', 'Nylon Carpet', 'Blended Carpet'")
        else:
            break

    while True:
        try:
            retail_cost = float(input("Enter the retail cost: "))
        except ValueError:
            print("Invalid number - please try again")
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

    # Calculations for customer purchase
    subtotal = retail_cost * quantity
    HST_amount = subtotal * HST
    order_total = subtotal + HST_amount
    order_date = today_str

    #  Increment order_number and put all purchase info into a list
    order_number += 1
    purchase_info.append((order_number, order_date, cust_num, item_num, description, retail_cost, quantity, subtotal, order_total, emp_number))

    # Open file and write back all data
    f = open("customerPurchase.dat", "a")
    for data in purchase_info:
        f.write(", ".join(map(str, data)) + "\n")
    f.close()


def option_five():

    print()
    print("Simpson's Carpet World")
    print(f"Employee Listing as of {today_str}")
    print("------------------------------------------------------------------------------")
    print("Employee #    Employee Name          Title                Branch        Salary")
    print("------------------------------------------------------------------------------")

    total_employees_acc = 0
    average_salary = 0
    total_salary_acc = 0

    f = open("employeeLog.dat", "r")
    for emp_data_line in f:
        emp_line = emp_data_line.split(",")

        employee_number = int(emp_line[0].strip())
        emp_first_name = emp_line[1].strip()
        emp_last_name = emp_line[2].strip()
        emp_branch = emp_line[9].strip()
        emp_title = emp_line[10].strip()
        emp_salary = float(emp_line[11].strip())
        full_name = emp_first_name + " " + emp_last_name

        print(f"{employee_number}          {full_name:<20s}   {emp_title:<16s}    {emp_branch:>4s}       "
              f"{FV.FDollar2(emp_salary):>10s}")

        total_employees_acc += 1
        total_salary_acc += emp_salary
        average_salary = total_salary_acc / total_employees_acc
    f.close()

    print("------------------------------------------------------------------------------")
    print(f"Total Employees: {total_employees_acc:>3d}    Average Salary: {FV.FDollar2(average_salary):>10s}   "
          f"Total Salary: {FV.FDollar2(total_salary_acc):>11s}")

    pass


def option_six():
    pass


def option_seven():
    pass


def option_eight():
    print()
    print("Simpson's Carpet World")
    print(f"Product Reorder Listing as of {today_str}")
    print("------------------------------------------------------------------------------")
    print("  Item #     Item Name        On Hand     Amt Ordered     Expected After Order")
    print("------------------------------------------------------------------------------")
    item_count = 0
    Order_amt = 0
    f = open('inventoryLog.dat', 'r')
    for item_data_line in f:
        item_line = item_data_line.split(',')
        item_num = int(item_line[0].strip())
        item_description = item_line[1].strip()
        retail_price = float(item_line[7].strip())
        QOH = int(item_line[8].strip())
        reorder_point = int(item_line[9].strip())
        max_amt = int(item_line[10].strip())

        while True:
            if QOH <= reorder_point:
                amt_need = max_amt - QOH
                Order_amt += (retail_price * amt_need)
                print(f'  {item_num:>4d}      {item_description:<14s}     {QOH:>4d}     {amt_need:>9d}   {max_amt:>15d}')
                QOH += amt_need
                item_count += 1
            elif QOH == max_amt:
                break
            break
    print("------------------------------------------------------------------------------")
    print(f"Total Items: {item_count:>2d}        Last Order: $30,000.00        Current Order: {FV.FDollar2(Order_amt)}")
    f.close()


while True:

    # Allow user to enter as many employees as needed, option to escape loop at end via input statement
    print()
    print("   Simpson Carpet World")
    print("  Company Services System")
    print()
    print('1. Enter a New Employee.')
    print('2. Enter a New Customer.')
    print('3. Enter a New Inventory Item.')
    print('4. Record Customer Purchase.')
    print('5. Print Employee Listing.')
    print('6. Print Customers By Branch.')
    print('7. Print Orders By Customer.')
    print('8. Print Recorder Listing.')
    print('9. Exit Menu')
    print()
    print()

    while True:
        try:
            choice = int(input("Please make a list selection: "))
        except ValueError:
            print("Please enter a valid number")
        else:
            if choice < 1 or choice > 9:
                print("Please enter a number from 1-9 to make a selection")
            else:
                break

    if choice == 1:
        print()
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
        print()
        print('Fourth option')
        print("-------------")
        option_four()
    elif choice == 5:
        print()
        print('Fifth option')
        print("-------------")
        option_five()
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
        print()
        print('Eighth option')
        print("-------------")
        option_eight()
    elif choice == 9:
        exit()
