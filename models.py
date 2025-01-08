'''from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class IndivPurchase(db.model):
    id = db.Column(db.integer, primary_key = True)
    user_id = db.Column(db.Interger, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    indivPurchase = db.relationship('IndivPurchase')'''