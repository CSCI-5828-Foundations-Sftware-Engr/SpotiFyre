import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100))
    email = sa.Column(sa.String(100), unique=True)
    password = sa.Column(sa.String(100))
    cache = sa.Column(sa.String(100), unique=True)

    # invitations_received = relationship('Invitation', backref='user', lazy=True)

class Tracks(Base):
    __tablename__ = 'tracks'

    track_id = sa.Column(sa.Integer, primary_key=True)
    track_uri = sa.Column(sa.String(100), nullable=False)
    track_name = sa.Column(sa.String(255), nullable=False)
    track_artist = sa.Column(sa.Integer, nullable=False)

class UserTracks(Base):
    __tablename__ = 'usertracks'

    ut_id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    track_id = sa.Column(sa.Integer, sa.ForeignKey('tracks.id'), nullable=False)

class Group(Base):
    __tablename__ = 'groups'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.String(255), nullable=False)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)

    # Define the relationship to the User model
    owner = relationship('User', backref='groups')

    #invitations_sent = relationship('Invitation', backref='group', lazy=True)
    # requests_received=  relationship('MembershipRequest', backref='user', lazy=True)


class Member(Base):
    __tablename__ = 'members'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)


# class Invitation(Base):
#     __tablename__ = 'invitations'

#     id = sa.Column(sa.Integer, primary_key=True)
#     user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
#     group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)
#     status = sa.Column(sa.String(10), default='pending')


class Playlist(Base):
    __tablename__ = 'playlists'
    id = sa.Column(sa.Integer, primary_key=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)
    playlist_name = sa.Column(sa.String(100))
    time_range = sa.Column(sa.String(50))
    genre = sa.Column(sa.String(50))
    # tags = sa.Column(sa.String(200))
    num_tracks = sa.Column(sa.Integer)
    link = sa.Column(sa.String(255), default=None)



