from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "SomeSecretKey"

account_balance = 0
stock_level = 0
history_list = []

@app.route("/")
def index_view():
    return render_template("index.html", balance=account_balance, stock=stock_level)

@app.route("/history", methods=["GET", "POST"])
def history_view():
    if request.method == "POST":
        filtered_history = history_list
        return render_template("history.html", history=filtered_history)
    else:
        return render_template("history.html", history=history_list)

@app.route("/purchase", methods=["GET", "POST"])
def purchase_view():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        try:
            price = int(price)
            quantity = int(quantity)
            if price <= 0 or quantity <= 0:
                raise ValueError("Price and quantity must be positive.")
            global stock_level, account_balance
            stock_level += quantity
            account_balance -= price * quantity
            add_history_entry(f"Purchased {quantity} {product_name} for {price}€ each")
            flash("Purchase successful!", category="success")
            return render_template("purchase.html")
        except ValueError as e:
            flash(f"Error: {e}", category="error")
    return render_template("purchase.html")

@app.route("/sell", methods=["GET", "POST"])
def sell_view():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        try:
            price = int(price)
            quantity = int(quantity)
            if price <= 0 or quantity <= 0:
                raise ValueError("Price and quantity must be positive.")
            global stock_level
            if stock_level < quantity:
                flash(f"Insufficient stock for {product_name}. Only {stock_level} available.", category="error")
                return render_template("sell.html")
            stock_level -= quantity
            global account_balance
            account_balance += price * quantity
            add_history_entry(f"Sold {quantity} {product_name} for {price}€ each")
            flash("Sold product successfully!", category="success")
            return render_template("sell.html")
        except ValueError as e:
            flash(f"Error: {e}", category="error")
            return render_template("sell.html")
    return render_template("sell.html")

@app.route("/balance", methods=["GET", "POST"])
def balance_view():
    if request.method == "POST":
        operation = request.form.get("operation")
        amount = request.form.get("amount")
        try:
            amount = int(amount)
            if operation == "add" and amount <= 0:
                raise ValueError("Amount must be positive for adding to balance.")
            global account_balance
            if operation == "add":
                account_balance += amount
            else:
                account_balance -= amount
            add_history_entry(f"Changed balance by {amount:}€")
            flash("Balance changed successfully!", category="success")
            return render_template("balance.html")
        except ValueError as e:
            flash(f"Error: {e}", category="error")
    return render_template("balance.html")

def add_history_entry(message):
    global history_list
    history_list.append({"message": message})