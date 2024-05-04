import json

warehouse = {}
operations = []
print(warehouse)

try:
    with open("warehouse.json",) as file_stream:
        warehouse = json.load(file_stream)
except FileNotFoundError:
    print("")

except ValueError:
    print("")

try:
    with open("balance.txt") as file_stream:
        balance_as_text = file_stream.read()
        balance = int(balance_as_text)
except FileNotFoundError:
    print("File does not exist, your balance will be 0.")
    balance = 0
except ValueError:
    print("You cannot convert this value to an integer. Setting balance to 0.")
    balance = 0

account_balance = balance
try:
    with open("operations.txt",) as file_stream:
        for line in file_stream:
            stripped_line = line.strip()
            if stripped_line == "":
                continue
            operations.append(stripped_line)
except FileNotFoundError:
    print("")

except ValueError:
    print("")

print("Commands:")
print("- balance\n""- sale\n""- purchase\n""- account\n""- list\n""- warehouse\n""- review\n""- end\n")

while True:
    command = input("Type a command to be performed:")

    if command == "balance":
        balance = str(input("Do you want to 'add' or 'subtract' balance from your account ?:"))

        if balance == "add":
            add = int(input("Enter the amount you want to add to your account balance:"))
            account_balance += add
            print(f"You have successfully added {add} $ to your account balance."
                  f"Your account balance is now {account_balance} $.\n")
            operations.append(f"Added {add} $ to account balance.")

        elif balance == "subtract":
            subtract = int(input("Enter the amount you want to subtract from your account balance:"))
            account_balance -= subtract
            if (account_balance-subtract) > 0:
                print(f"You have successfully subtracted {subtract} $ from your account balance."
                      f"Your account balance is now {account_balance} $.\n")
                operations.append(f"Subtracted {subtract} $ from account balance.")
            if (account_balance-subtract) < 0:
                print(f"Insufficient balance.Your account balance is {account_balance}.")

        else:
            print("Invalid command.")

    elif command == "account":
        print(f"Your account balance is {account_balance} $.\n")

    elif command == "sale":
        product = input("Enter product name:")
        price = int(input("Enter price per unit:"))
        quantity = int(input("Enter units sold:"))
        if product in warehouse and warehouse[product]["quantity"] >= quantity:
            total_price = price * quantity
            warehouse[product]["quantity"] -= quantity
            account_balance += total_price
            print(f"Sold {quantity} {product} for {total_price}$.")
            operations.append(f"{quantity} units of {product} sold for {total_price} $.")

    elif command == "purchase":
        product = input("Enter product name:")
        price = int(input("Enter price per unit:"))
        quantity = int(input("Enter units purchased:"))
        total_price = price * quantity
        account_balance -= total_price
        if account_balance > 0:
            if product in warehouse:
                warehouse[product]["quantity"] += quantity
                for product, details in warehouse.items():
                    print(f"{product}: {details["quantity"]} units - ${details["price"]} per unit")
            else:
                warehouse[product] = {"price": price, "quantity": quantity}
                for product, details in warehouse.items():
                    print(f"{product}: {details['quantity']} units - ${details['price']} per unit")
            print(f"Purchased {quantity} {product} for {total_price}$")
            operations.append(f"{quantity} units of {product} purchased for {total_price} $.")

    elif command == "warehouse":
        product = input("Enter product name: ")
        if product in warehouse:
            print(f"{product}: {details['quantity']} units - ${details['price']} per unit")
        else:
            print("Product not available at the moment.")

    elif command == "list":
        for product, details in warehouse.items():
            print(f"{product}: {details['quantity']} units - ${details['price']} per unit")

    elif command == "review":
        from_ = int(input("Enter 'from' index:"))
        to = int(input("Enter 'to' index:"))
        if len(operations) >= from_ >= 0 and len(operations) >= to > 0:
            print("")
            print("Recorded operations:")
            for line in operations[from_:to]:
                print(line)
            print("")
        elif from_ == 0 and to == 0:
            print("")
            print("Recorded operations:")
            for line in operations:
                print(line)
            print("")
        elif from_ < 0 and to < 0:
            print("You can't enter negative numbers.")
        else:
            print(f"Invalid index range.Minimum index range is 0 and maximum index range is {len(operations)}.")

    elif command == "end":
        break

    else:
        print("Invalid command.\n")
        continue

    with open("balance.txt", mode="w") as file_stream:
        file_stream.write(str(account_balance))

    with open("operations.txt",mode="w") as file_stream:
        for operation in operations:
            file_stream.write(f"{operation}\n")

    with open("warehouse.json", mode="w") as file_stream:
        json.dump(warehouse, file_stream)
