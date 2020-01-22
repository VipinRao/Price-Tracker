from pricetracker import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import url_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    #add columns for table
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True,nullable = False)
    image_file = db.Column(db.String(40), nullable = False, default= 'default.png')
    password = db.Column(db.String(200),nullable = False)
    url = db.relationship('Rating', backref='author', lazy=True)

    def __repr__(self): #for printing
        return f"User('{self.username}','{self.email}','{self.password}')"

class Check_request(db.Model):
    url = db.Column(db.String(1000),nullable = False,primary_key = True)
    target_price = id = db.Column(db.Integer)

class Rating(db.Model): #url -> user_ids searching for this product
    #add columns for table
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): #for printing
        return f"User('{self.username}','{self.email}','{self.password}')"
