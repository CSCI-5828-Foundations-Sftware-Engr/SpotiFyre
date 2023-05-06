from . import db
from flask_login import UserMixin


from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    cache = db.Column(db.String(100), unique=True, default='default-cache')

    invitations_received = db.relationship('Invitation', backref='user', lazy=True)


class Group(UserMixin, db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define the relationship to the User model
    owner = relationship('User', backref='groups')

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

class Member(UserMixin, db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    

class Tracks(UserMixin, db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    track_uri = db.Column(db.String(100), nullable=False)
    track_name = db.Column(db.String(255), nullable=False)
    track_artist = db.Column(db.Integer, nullable=False)

class UserTracks(UserMixin, db.Model):
    __tablename__ = 'usertracks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)


class Playlist(UserMixin, db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    playlist_name = db.Column(db.String(100))
    num_tracks = db.Column(db.Integer)
    link = db.Column(db.String(255), default=None)

