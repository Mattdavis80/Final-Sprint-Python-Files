import re
import datetime

today = datetime.datetime.now()
today_str = datetime.datetime.strftime(today, "%m/%d/%Y")

valid_prov = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
# Read data from the file defaults.dat
f = open('defaults.dat', 'r')
employee_num = int(f.readline())
inventory_num = int(f.readline())
commission_rate = float(f.readline())
bonus_threshold = float(f.readline())
commission_bonus_amt = float(f.readline())
reorder_num = int(f.readline())
HST = float(f.readline())
f.close()

def option_one():
    # User Validated Inputs
    # First name, mandatory input, alpha only, converted to Title-case
    employee_info = []
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

    # City, mandatory input, converted to Title-case -------- need to make exception for '--------------
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
        elif not prov in valid_prov:
            print("Please enter a valid province")
        else:
            break

    # Postal Code, mandatory input, must be valid format as X0X 0X0 ------ADD REPLACE STATEMENTS
    # The pattern below is used to compare against user input, this will be done using Regular Expressions
    # The pattern will accept a space or dash between postal code
    pattern = r"^[A-Z]\d[A-Z][ -]?\d[A-Z]\d$"

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
            formatted_phone_num = phone_num[:3] + "-" + phone_num[3:6] + "-" + phone_num[6:]
            break

    # Date hired, mandatory input, valid date
    while True:
        try:
            date_hired = input("Please enter date hired as dd-mm-yyyy: ")
            # date_hired = datetime.datetime.strftime(%d-%m-%Y)
            break
        except:
            print("You make fucking mistake in the date of hiring, common")

    employee_info.append((employee_num.strip(), emp_f_name, emp_l_name, str_add, city, prov, post_code, phone_num))
    employee_info[0] += 1
    f = open('employeeLog.dat', 'a')
    for data in employee_info:
        f.write(",".join(map(str, data)) + "\n")
    f.close()

    pass


def option_two():
    customer_info = []

    pass


def option_three():
    pass


item_file = open('inventoryLog.dat', 'r')

item_numbers_list = []
item_descriptions_list = []
for item_data_line in item_file:
    item_line = item_data_line.split(',')

    item_number = int(item_line[0].strip())
    item_description = item_line[1].strip()
    retail_price = item_line[7].strip()

    item_numbers_list.append(item_number)
    item_descriptions_list.append(item_description)


item_file.close()

employee_file = open("employeeLog.dat", "r")

emp_numbers_list = []

for employee_data_line in employee_file:
    employee_line = employee_data_line.split(',')

    employee_num = employee_line[0].strip()

    emp_numbers_list.append(employee_num)

employee_file.close()

f = open("customerLog.dat", "r")

customer_numbers_list = []
for customer_data_line in f:
    customer_line = customer_data_line.split(',')

    customer_number = int(customer_line[0].strip())

    customer_numbers_list.append(customer_number)

f.close()

purchase_file = open("customerPurchase.dat", "r")

for purchase_data_line in purchase_file:
    purchase_line = purchase_data_line.split(',')

    order_number = int(purchase_line[0].strip())

purchase_file.close()


def option_four():
    purchase_info = []
    print("Enter new order information")

    while True:
        emp_number = input("Employee Number: ")
        if emp_number == "":
            print("Cannot be blank - please try again.")
        elif emp_number not in emp_numbers_list:
            print("Does not match any current employee number - please try again.")
        else:
            break

    while True:
        # our customerLog file contains customer numbers of 4000 - 4005
        # so this section should only work if entering 4000 - 4005
        customer_num = int(input("Customer Number: "))
        if customer_num not in customer_numbers_list:
            new_cust_msg = input("Customer does not exist - would you like to add a new customer? (Y/N): ").upper()
            if new_cust_msg != "Y" and new_cust_msg != "N":
                print("Invalid input - please enter 'Y' or 'N'")
            elif new_cust_msg == "Y":
                option_two()
                # of course this won't actually add a new customer because we only had to
                # do option 1 or 2 or 3 and option 1 is done, so I didn't actually code option_two()
                # Let's pretend this actually added a new customer then get sent back up
                # to ask for customer number again, where we can enter 4000 - 4005 to continue
            else:
                continue
        else:
            break

    while True:
        try:
            item_num = int(input("Item Number: "))
        except ValueError:
            print("Invalid input - must enter an integer.")
        else:
            if item_num not in item_numbers_list:
                print("That item number does not match any of our items - please try again.")
            else:
                break

    while True:
        description = input("Item Description: ")
        if description == "":
            print("Cannot be blank - please try again.")
        elif description not in item_descriptions_list:
            print("We do not sell any items of that description - please try again.")
            print("Here's a list of valid descriptions: ")
            print("'Wool Carpet', 'Nylon Carpet', 'Blended Carpet'")
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

    # calculations for customer purchase
    subtotal = retail_cost * quantity
    HST_amount = subtotal * HST
    order_total = subtotal + HST_amount

    order_date = today_str

    # Put all purchase info into list
    purchase_info.append((order_number, order_date, customer_num, item_num, description, retail_cost, quantity, subtotal, order_total, emp_number))
    purchase_info[0] += 1   # Increment order_number before writing it back
    # Open file and write back all data
    order_file = open("customerPurchase.dat", "a")

    for data in purchase_info:
        order_file.write(",".join(map(str, data)) + "\n")
    order_file.close()

    pass


def option_five():
    pass


def option_six():
    pass


def option_seven():
    pass


def option_eight():
    pass

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
    print('7. Print Orders By Customer,.')
    print('8. Print Recorder Listing.')
    print('9. Exit Menu')
    print()
    print()

    while True:
        try:
            choice = int(input("Please make a list selection: "))
        except:
            print("Please enter a valid number")
        else:
            if choice < 1 or choice > 9:
                print("Please enter a number from 1-9 to make a selection")
            else:
                break

    if choice == 1:
        print()
        print('First option')
        print("-------------")
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
