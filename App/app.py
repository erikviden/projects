from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next-page")
def next_page_view():
    return render_template("next-page.html")