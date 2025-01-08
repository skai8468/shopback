from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    general_stamps = db.Column(db.Integer, default=0)
    purchases = db.relationship('Purchase', backref='user', lazy=True)

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(255), unique=True, nullable=False)
    purchases = db.relationship('Purchase', backref='store', lazy=True)

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store_stamps = db.Column(db.Integer, default=0)
    purchase_count = db.Column(db.Integer, default=0)
    last_purchase = db.Column(db.DateTime)