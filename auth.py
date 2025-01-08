from flask import Blueprint, render_template, request, jsonify
from .model import User, db 

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

@auth.route('/add_data', methods=['POST'])
def add_data():
    # Extract data from the request
    user_id = request.json.get('user_id')
    general_stamps = request.json.get('general_stamps', 0)

    # Validate input
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Create a new user instance
    new_user = User(user_id=user_id, general_stamps=general_stamps)

    try:
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Data added successfully!", "user": user_id}), 201
    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        return jsonify({"error": str(e)}), 400