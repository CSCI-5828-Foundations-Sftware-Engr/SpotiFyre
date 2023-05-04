from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import psycopg2
from flask_login import LoginManager
import os 

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
host = os.getenv('PQ_HOST', "postgres-db-postgresql")
port = os.getenv('PQ_PORT', "5432")
user = os.getenv('PQ_USER', "root")
passWd = os.getenv('PQ_PASS', "algo123")
pqdb = os.getenv('PQ_DB', "spotifyre_db")

def create_app():
    global app
    app = Flask(__name__)

    url = f'postgresql://{user}:{passWd}@{host}:{port}/{pqdb}'
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    app.config['SQLALCHEMY_DATABASE_URI'] = url
    db.init_app(app)
    try:
        conn = psycopg2.connect(
            database=pqdb, user=user, password=passWd, host=host, port=port)
    except Exception as e:
        print(e)
        exit(0) 

    cur = conn.cursor()
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Users (id serial PRIMARY KEY, name varchar NOT NULL, email varchar NOT NULL, password varchar NOT NULL, cache varchar DEFAULT 'default-cache');")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Groups (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, description VARCHAR(255) NOT NULL, owner_id INTEGER NOT NULL, FOREIGN KEY (owner_id) REFERENCES users (id));")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Invitations (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, group_id INTEGER NOT NULL, status VARCHAR(10) DEFAULT 'pending', FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (group_id) REFERENCES groups (id));")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Membership_Requests (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, group_id INTEGER NOT NULL,status VARCHAR(10) DEFAULT 'pending', FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (group_id) REFERENCES groups (id));")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Members (id serial PRIMARY KEY,  user_id INTEGER NOT NULL, group_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (id), FOREIGN KEY (group_id) REFERENCES Groups (id));")            
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Tracks (id serial PRIMARY KEY, track_uri varchar NOT NULL, track_name varchar NOT NULL, track_artist varchar NOT NULL);") # , track_genres varchar
        cur.execute(
            "CREATE TABLE IF NOT EXISTS UserTracks (id serial PRIMARY KEY, user_id int REFERENCES Users(id)  NOT NULL, track_id int REFERENCES Tracks(id) NOT NULL);")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Playlists (id serial PRIMARY KEY, group_id INTEGER NOT NULL, playlist_name varchar NOT NULL, num_tracks INTEGER, link varchar, FOREIGN KEY (group_id) REFERENCES groups (id));")
    except Exception as e:
        print(e)
        exit(0) 

    conn.commit()  # <--- makes sure the change is shown in the database
    conn.close()
    cur.close()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Tracks, UserTracks


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for spotify parts of app
    from .spotify_login import spotify_login as spotify_login_blueprint
    app.register_blueprint(spotify_login_blueprint)

    return app
