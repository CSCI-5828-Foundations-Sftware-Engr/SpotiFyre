import json
from flask import Flask, render_template, request, redirect, session, Blueprint, jsonify
from flask_login import login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Playlist
from . import db
from google.cloud import pubsub_v1
import os

playlist = Blueprint('playlist', __name__)

# Configure the Google Cloud project and Pub/Sub topic
project_id = os.getenv('PROJECT', "polished-time-381400")
topic_name = os.getenv('TOPIC_PLAYLIST', "playlist-parameters")

@playlist.route('/generate_playlist', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        group_id = int(request.form['group-id'])
        playlist_name = request.form['playlist-name']
        # time_range = request.form['time-range']
        # genre = request.form['genre']
        # tags = request.form['tags']
        num_tracks = int(request.form['num-tracks'])

        # Generate the playlist based on the form input

        # Create a new playlist parameters object
        playlist_params = Playlist(
            group_id=group_id,
            playlist_name=playlist_name,
            # time_range=time_range,
            # genre=genre,
            #tags=tags,
            num_tracks=num_tracks,
        )

        # Save the playlist parameters to the database
        db.session.add(playlist_params)
        db.session.commit()

        # Convert the dictionary to JSON
        json_data = json.dumps(playlist_params)

        # Publish the JSON data to the Pub/Sub topic
        try :

            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_name)
            print(f'Publishing to the queue {topic_name}')
            publisher.publish(topic_path, data=json_data.encode())

            response = {'success': True, 'message': 'Playlist record created', 'data' : playlist_params.id}
            return jsonify(response)

            # Need to decide if the frontend calls get_playlist_link or if it's called here

        except  Exception as e:
            print("Failed to publish", e )
            response = {'success': False, 'message': 'Could not create the playlist. Try again'}
            return jsonify(response)


@playlist.route('/get_playlist_link', methods=['GET', 'POST'])
def get_playlist_link():
    playlist_id = request.form.get('playlist_id')

    # Query the Playlist table for the link based on the group_id
    playlist = Playlist.query.filter_by(id=playlist_id).first()

    if playlist is None or playlist.link is None:
        response = {'success': False, 'message': 'Link not present'}
        return jsonify(response)

    response = {'success': False, 'message': 'Created playlist link', 'data' : playlist.link}
    return jsonify(response)
