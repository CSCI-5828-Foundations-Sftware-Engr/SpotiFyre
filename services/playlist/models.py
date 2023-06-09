import sqlalchemy as db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    cache = db.Column(db.String(100), unique=True, default='default-cache')

    invitations_received = relationship('Invitation', backref='user', lazy=True)
    #requests_sent = relationship('MembershipRequest', backref='user', lazy=True)

class Group(Base):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define the relationship to the User model
    owner = relationship('User', backref='groups')

    #invitations_sent = relationship('Invitation', backref='group', lazy=True)
    requests_received=  relationship('MembershipRequest', backref='user', lazy=True)


class Invitation(Base):
    __tablename__ = 'invitations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    status = db.Column(db.String(10), default='pending')

class MembershipRequest(Base):
    __tablename__ = 'membership_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    status = db.Column(db.String(10), default='pending')

class Member(Base):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    

class Tracks(Base):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    track_uri = db.Column(db.String(100), nullable=False)
    track_name = db.Column(db.String(255), nullable=False)
    track_artist = db.Column(db.Integer, nullable=False)

class UserTracks(Base):
    __tablename__ = 'usertracks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)


class Playlists(Base):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    playlist_name = db.Column(db.String(100))
    num_tracks = db.Column(db.Integer)
    link = db.Column(db.String(255), default=None)
