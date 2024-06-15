from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "SomeSecretKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Integer)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)


def add_history_entry(message):
    transaction = Transaction(message=message)
    db.session.add(transaction)
    db.session.commit()

with app.app_context():
    db.create_all()
@app.route("/")
def index_view():
    current_balance = Balance.query.get(1)
    stock_levels = Product.query.all()
    db.session.commit()
    return render_template("index.html", balance=current_balance.amount, stock=stock_levels)

@app.route("/balance", methods=["GET", "POST"])
def balance_view():
    current_balance = Balance.query.get(1)
    if request.method == "POST":
        new_balance = request.form.get("new_balance")
        try:
            new_balance = int(new_balance)
            current_balance.amount = new_balance
            db.session.commit()
            flash("Balance updated successfully!", category="success")
        except ValueError:
            flash("Invalid balance value. Please enter an integer.", category="error")
    db.session.commit()
    return render_template("balance.html", balance=current_balance.amount)
@app.route("/history", methods=["GET", "POST"])
def history_view():
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()
    if request.method == "POST":
        filtered_history = [t for t in transactions if request.form.get("filter") in t.message]
        return render_template("history.html", history=filtered_history)
    else:
        return render_template("history.html", history=transactions)

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
            product = Product.query.filter_by(name=product_name).first()
            if not product:
                product = Product(name=product_name, quantity=0)
                db.session.add(product)
            product.quantity += quantity
            current_balance = Balance.query.get(1)
            current_balance.amount -= price * quantity
            add_history_entry(f"Purchased {quantity} {product_name} for {price}€ each")
            try:
                db.session.commit()
                flash("Purchase successful!", category="success")
                return render_template("purchase.html")
            except Exception as e:
                flash(f"An error occurred: {e}", category="error")
        except ValueError as e:
            flash(f"Error: {e}", category="error")
    products = Product.query.all()
    db.session.commit()
    return render_template("purchase.html", products=products)

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
            product = Product.query.filter_by(name=product_name).first()
            if not product or product.quantity < quantity:
                flash(f"Insufficient stock for {product_name}. Only {product.quantity if product else 0} available.", category="error")
                return render_template("sell.html")
            product.quantity -= quantity
            current_balance = Balance.query.get(1)
            current_balance.amount += price * quantity
            add_history_entry(f"Sold {quantity} {product_name} for {price}€ each")
            try:
                db.session.commit()
                flash("Sold product successfully!", category="success")
                return render_template("sell.html")
            except Exception as e:
                flash(f"An error occurred: {e}", category="error")
        except ValueError as e:
            flash(f"Error: {e}", category="error")
        products = Product.query.all()
        db.session.commit()
        return render_template("sell.html", products=products)
