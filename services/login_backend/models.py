from . import db
from flask_login import UserMixin

from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    invitations_received = db.relationship('Invitation', backref='user', lazy=True)
    #requests_sent = db.relationship('MembershipRequest', backref='user', lazy=True)

class Group(UserMixin, db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define the relationship to the User model
    owner = relationship('User', backref='groups')

    #invitations_sent = db.relationship('Invitation', backref='group', lazy=True)
    requests_received=  db.relationship('MembershipRequest', backref='user', lazy=True)


class Invitation(UserMixin, db.Model):
    __tablename__ = 'invitations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    status = db.Column(db.String(10), default='pending')

class MembershipRequest(UserMixin, db.Model):
    __tablename__ = 'membership_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    status = db.Column(db.String(10), default='pending')