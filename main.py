import random

from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask (__name__)
db.create_all()

@app.route("/", methods=["GET"])
def index():
    email = request.cookies.get("email")
    if email:
        user = db.query(User).filter_by(email=email).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user")
    email = request.form.get("email")
    password = request.form.get("password")

    secret_number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number, password=password)

        db.add(user)
        db.commit()

    if password != user.password:
        return "WRONG PASSWORD! Go back and try again"

    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    email = request.cookies.get("email")

    user = db.query(User).filter_by(email=email).first()

    if guess == user.secret_number:
        message = "Congratulations! Your guess is correct. The secret number is {}".format(str(guess))

        new_secret = random.randint(1, 30)
        user.secret_number = new_secret

        db.add(user)
        db.commit()

    elif guess > user.secret_number:
        message = "I am sorry but your guess is wrong. Try something lower"
    elif guess < user.secret_number:
        message = "I am sorry but your guess is wrong. Try something higher"

    return render_template("result.html", message=message)

if __name__ == '__main__':
    app.run()