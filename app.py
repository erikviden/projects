from flask import Flask, render_template, url_for

app = Flask(__name__)

account_balance = 12000
text_list = ["Text1", "text2", "text3"]

@app.route("/")
def index():
    return render_template("index.html", balance=account_balance, text_list=text_list)

@app.route("/history", methods=["GET","POST"])
def history():
    return render_template("history.html")

@app.route("/purchase", methods=["GET","POST"])
def purchase():
    return render_template("purchase.html")

@app.route("/sell", methods=["GET","POST"])
def sell():
    return render_template("sell.html")

@app.route("/balance", methods=["GET","POST"])
def balance():
    return render_template("balance.html")