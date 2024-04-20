warehouse = {}
account_balance = 0
operations = []

print("Commands:")
print("- balance\n""- sale\n""- purchase\n""- account\n""- list\n""- warehouse\n""- review\n""- end\n")

while True:
    command = input("Type a command to be performed:")

    if command == "balance":
        balance = str(input("Do you want to 'add' or 'subtract' balance from your account ?:"))

        if balance == "add":
            add = float(input("Enter the amount you want to add to your account balance:"))
            account_balance += add
            account_balance = round(account_balance, 2)
            print(f"You have successfully added {add} $ to your account balance."
                  f"Your account balance is now {account_balance} $.\n")
            operations.append(f"Added {add} $ to account balance.")

        elif balance == "subtract":
            subtract = float(input("Enter the amount you want to subtract from your account balance:"))
            if (account_balance-subtract) > 0:
                account_balance = round(account_balance, 2)
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
        price = round(price, 2)
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
        price = round(price, 2)
        total_price = price * quantity
        account_balance -= total_price
        if account_balance > 0:
            if product in warehouse:
                warehouse[product]["quantity"] += quantity
            else:
                warehouse[product] = {"price": price, "quantity": quantity}
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
            print("Recorded operations:")
            print(operations[from_:to])
        elif from_ == 0 and to == 0:
            print("Recorded operations:")
            print(operations)
        elif from_ < 0 and to < 0:
            print("You can't enter negative numbers.")
        else:
            print(f"Invalid index range.Minimum index range is 0 and maximum index range is {len(operations)}.")

    elif command == "end":
        break

    else:
        print("Invalid command.\n")
        continue
