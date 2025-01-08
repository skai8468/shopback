from flask import Blueprint, render_template, request

auth = Blueprint('auth ', __name__)


@auth.route('/home')
def home():
    return render_template("homepage.html")

@auth.route('/buy', methods= ['GET', 'POST'])
def buy():
    data = request.form
    return render_template("payment.html")

@auth.route('/stampcard')
def stampcard():
    return render_template("stampcard.html")