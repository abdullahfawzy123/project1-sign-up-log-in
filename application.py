import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL", "postgres://dxzgqblzlqbrjv:8a3849a2dfeb682893f7e056dbeafaf81effece7fc4caf35952edf6a65a88e1d@ec2-54-165-36-134.compute-1.amazonaws.com:5432/da2pvgscfo55q4"))
db = scoped_session(sessionmaker(bind=engine))

def add_account():
    db.execute("INSERT INTO accounts (username, password) VALUES (username, password)")


def main():
    @app.route("/")
    def index():
        return render_template("welcome.html")


    accounts = db.execute("SELECT * FROM accounts").fetchall()

    @app.route("/sign_up", methods=["POST"])
    def sign_up():
        username = request.form.get("username")
        password = request.form.get("password")
        c_password = request.form.get("c_password")

        available_username = db.execute("SELECT * FROM accounts WHERE username = :username", {"username": username}).rowcount == 0
        taken_username = db.execute("SELECT * FROM accounts WHERE username = :username", {"username": username}).rowcount == 1

        if available_username and password == c_password:
            add_account()
            return render_template("homepage.html", username="username")

        elif taken_username:
            return render_template("sign_up.html", message="username is already taken")

        else:
            return render_template("sign_up.html", message="password and confirm password are not the same")

    @app.route("/log_in", methods=["POST"])
    def log_in():
        username = request.form.get("username")
        password = request.form.get("password")

        correct_username_password = db.execute("SELECT * FROM accounts WHERE username = :username, password = :password", {"username": username, "password": password})
        incorrect_password = db.execute("SELECT * FROM accounts WHERE username = :username, password != :password", {"username": username, "password": password})
        if correct_username_password :
            return render_template("homepage.html", username="username")

        elif incorrect_password :
            return render_template("log_in.html", message="password incorect")
        else:
            return render_template("log_in.html", message="username not found")



if __name__ == '__main__':
    main()
