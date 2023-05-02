from . import db
from flask_login import UserMixin



class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Playlist(UserMixin, db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    playlist_name = db.Column(db.String(100))
    time_range = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    # tags = db.Column(db.String(200))
    num_tracks = db.Column(db.Integer)
    link = db.Column(db.String(255), default=None)



