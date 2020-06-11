import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL", "postgres://dxzgqblzlqbrjv:8a3849a2dfeb682893f7e056dbeafaf81effece7fc4caf35952edf6a65a88e1d@ec2-54-165-36-134.compute-1.amazonaws.com:5432/da2pvgscfo55q4"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("welcome.html")


accounts = db.execute("SELECT * FROM accounts").fetchall()

@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    username = request.form.get("username")
    password = request.form.get("password")


    available_username = db.execute("SELECT * FROM accounts WHERE username != :username", {"username": username})
    taken_username = db.execute("SELECT * FROM accounts WHERE username = :username", {"username": username})

    if available_username:
        add_account()
        return render_template("homepage.html", username="username")


    elif taken_username:
        return render_template("welcome.html", message="username is already taken")


@app.route("/log_in", methods=["POST", "GET"])
def log_in():
    username = request.form.get("username")
    password = request.form.get("password")

    correct_username_password = db.execute("SELECT * FROM accounts WHERE username = :username, password = :password", {"username": username, "password": password})
    incorrect_password = db.execute("SELECT * FROM accounts WHERE username = :username, password != :password", {"username": username, "password": password})
    if correct_username_password :
        return render_template("homepage.html", username="username")

    elif incorrect_password :
        return render_template("welcome.html", message1="password incorect")
    else:
        return render_template("welcome.html", message1="username not found")



def add_account():
    db.execute("INSERT INTO accounts (username, password) VALUES (username, password)", {"username": username, "password": password})

if __name__ == '__main__':
    app.run()
