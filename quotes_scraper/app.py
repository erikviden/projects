from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)

class QuotesTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String)
    tags = db.Column(db.String)
    author = db.Column(db.String)

with app.app_context():
    db.create_all()

def scrape():
    url = "https://quotes.toscrape.com/page/{}/"
    for page in range(1, 11):
        response = requests.get(url.format(page))
        soup = BeautifulSoup(response.content, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = ", ".join(tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag"))
            if not QuotesTable.query.filter_by(quote=text).first():
                new_quote = QuotesTable(quote=text, author=author, tags=tags)
                db.session.add(new_quote)
        db.session.commit()

@app.route("/")
def index():
    quotes = QuotesTable.query.all()
    return render_template("index.html", quotes=quotes)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form.get("search")
        filter_by = request.form.get("filter_by")
        if filter_by == "author":
            quotes = QuotesTable.query.filter(QuotesTable.author.like(f"%{search_query}%")).all()
        elif filter_by == "tag":
            quotes = QuotesTable.query.filter(QuotesTable.tags.like(f"%{search_query}%")).all()
        else:
            quotes = []
        return render_template("index.html", quotes=quotes)
    return redirect(url_for("index"))

@app.route("/random")
def random_quote():
    quotes = QuotesTable.query.all()
    if quotes:
        quote = random.choice(quotes)
        return render_template("index.html", quotes=[quote])
    return render_template("index.html", quotes=[])

if __name__ == "__main__":
    with app.app_context():
        scrape()
    app.run(debug=True)