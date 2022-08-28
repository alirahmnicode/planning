from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))
    groups = db.relationship('Group', backref='user')
    items = db.relationship('Plan', backref='user')
    habits = db.relationship('Habit', backref='user')


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text())
    is_done = db.Column(db.Boolean())
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def delete_obj(self):
        db.session.delete(self)
        db.session.commit()
        
    def save(self):
        db.session.add(self)
        db.session.commit()


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Plan', backref='group')
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.Text())
    active = db.Column(db.Boolean(), default=True)
    expiration = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()