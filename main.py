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
VALID_PROV = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
BRANCH_LIST = ["St. John's", "Mt. Pearl", "Carbonear", "Northern Bay"]

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


def option_one():
    """A function that will enter a new employee's information, then
    append it all into the employee file as a new record."""

    while True:
        global employee_num
        employee_info = []

        # User Validated Inputs
        # First name, mandatory input, alpha only, converted to Title-case
        while True:
            emp_f_name = input("First Name: ").title()
            if emp_f_name == "":
                print("First name cannot be empty, Please re-enter")
            elif not emp_f_name.isalpha():
                print("Please enter a valid name")
            else:
                break

        # Last name, mandatory input, alpha only, converted to Title-case
        while True:
            emp_l_name = input("Last Name: ").title()
            if emp_l_name == "":
                print("Last name cannot be empty, Please re-enter")
            elif not emp_l_name.isalpha():
                print("Please enter a valid name")
            else:
                break

        # Street Address, mandatory input, converted to Title-case
        while True:
            str_add = input("Street Address: ").title()
            if str_add == "":
                print("Street address cannot be empty, Please re-enter")
            else:
                break

        # City, mandatory input, converted to Title-case
        while True:
            city = input("City: ").title()
            if city == "":
                print("City cannot be empty, Please re-enter")
            else:
                break

        # Province, mandatory input,converted to Upper-case, compared to valid list of provinces
        while True:
            prov = input("Province (XX): ").upper()

            if len(prov) != 2:
                print("Please re-enter province as (XX)")
            elif prov == "":
                print("Province field cannot be empty, Please re-enter")
            elif prov not in VALID_PROV:
                print("Please enter a valid province")
            else:
                break

        # Postal Code, mandatory input, must be valid format as X0X 0X0
        # The pattern below is used to compare against user input, this will be done using Regular Expressions
        # The pattern will accept a space or dash between postal code
        pattern = r"^[A-Z]\d[A-Z] \d[A-Z]\d$"

        while True:
            post_code = input("Postal Code: (e.g. A1A 1A1):   ").upper()
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
                emp_salary = float(input("Employee Salary: "))
                emp_salary = round(emp_salary, 2)
            except ValueError:
                print("Please enter a valid number")
            else:
                if emp_salary < 13000:
                    print("This salary is below minimum wage, please re-enter")
                elif emp_salary > 100000:
                    print("This salary is above the highest paid person at Sampson's Carpet, Please re-enter")
                else:
                    break

        # Employee Skills, mandatory input, alpha only
        while True:
            emp_skills = input("Employee skill: ").title()
            if not emp_skills.isalpha():
                print("Please enter valid skill")
            else:
                break

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
    print("Employee #    Employee Name          Title               Branch        Salary")
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

        print(f"{employee_number}          {full_name:<20s}   {emp_title:<16s}    {emp_branch:>6s}     "f"{FV.FDollar2(emp_salary):>10s}")

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


def problem_solving():
    if today.day == 1:
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

        # calculate the commission for each employee and display the results
        unique_emp_ids = set(sales_totals.keys())
        print(f'Commission totals for {len(unique_emp_ids)} employees as of {today.year}-{today.month:02d}-{today.day:02d}:')
        for emp_id in unique_emp_ids:
            sales_total = sales_totals[emp_id]
            commission = 0.06 * sales_total
            if sales_total > 5000:
                commission += 200
            print(f'Employee {emp_id}: ${commission:.2f}')
    else:
        print('Commission calculation only runs on the first day of the month.')


while True:
    problem_solving()
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