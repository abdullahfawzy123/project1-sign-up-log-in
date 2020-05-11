import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("postgres://postgres:01285502660@localhost:5432"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("home_page.html")

accounts = db.execute("SELECT * FROM accounts").fetchall()

@app.route("/sign_up_render", methods=["POST"])
def sign_up_render():
    return render_template("sign_up.html")


@app.route("/sign_up")
def sign_up():
    username = request.form.get("username")
    password = request.form.get("password")
    c-password = request.form.get("c-password")

    if db.execute("SELECT * FROM accounts WHERE username = :username").rowcount == 0 and password == c-password:
        db.execute("INSERT INTO accounts (username, password) VALUES (:username, :password)")
        return render_template("welcome.html", username="username") 

    elif db.execute("SELECT * FROM accounts WHERE username = :username").rowcount == 1:
        return render_template("sign_up.html", message="username is already taken")

    else:
        return render_template("sign_up.html", message="password and confirm password are not the same")


@app.route("/log_in_render", methods=["POST"])
def log_in_render():
    return render_template("log_in.html")


@app.route("/log_in", methods=["POST"])
def log_in():
    username = request.form.get("username")
    password = request.form.get("password")

    if db.execute("SELECT * FROM accounts WHERE username = :username, password = :password"):
        return render_template("welcome.html", username="username")

    elif db.execute("SELECT * FROM accounts WHERE username = :username, password =! :password"):
        return render_template("log_in.html", message="password incorect")

    else:
        return render_template("log_in.html", message="username not found")
