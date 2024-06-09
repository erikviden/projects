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
def history_view(start=0, end=0, history_list= history_list):
    if end != 0 and start!= 0:
        history_list = history_list[start:end]
    else:
        history_list = history_list
    return render_template("history.html", history=history_list)


@app.route("/purchase", methods=["GET", "POST"])
def purchase_view():
    return render_template("purchase.html")


@app.route("/sell", methods=["GET", "POST"])
def sell_view():
    return render_template("sell.html")


@app.route("/balance", methods=["GET", "POST"])
def balance_view():
    return render_template("balance.html")
