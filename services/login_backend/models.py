from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    cache = db.Column(db.String(100), unique=True)

class Tracks(UserMixin, db.Model):
    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer, primary_key=True)
    track_uri = db.Column(db.String(100), nullable=False)
    track_name = db.Column(db.String(255), nullable=False)
    track_artist = db.Column(db.Integer, nullable=False)

class UserTracks(UserMixin, db.Model):
    __tablename__ = 'usertracks'

    ut_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)
