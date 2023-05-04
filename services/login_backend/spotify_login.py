import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, redirect, jsonify, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from .models import User, Tracks, UserTracks
from . import db

spotify_login = Blueprint('spotify_login', __name__)

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
scope = os.getenv('SPOTIFY_SCOPE')

print(client_id, client_secret, redirect_uri, scope)

# Create a Spotipy instance with a new cache path for each user
def create_spotify_instance(cache_path):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                      client_secret=client_secret,
                                                      redirect_uri=redirect_uri,
                                                      scope=scope,
                                                      cache_path=cache_path))

# Endpoint for initiating the Spotify authentication flow
@spotify_login.route('/spotify-login')
def login():
    print('Login endpoint')
    # Get the cache path for this user
    user_id = session.get('user_id')
    cache_path = f'.cache-{user_id}'

    # Create a new Spotipy instance with the cache path
    sp = create_spotify_instance(cache_path)
    
    # Redirect the user to the Spotify login page
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

# Endpoint for retrieving the access token after the user has logged in
@spotify_login.route('/callback')
def callback():
    print('callback endpoint')
    # Get the cache path for this user
    user_id = session.get('user_id')
    cache_path = f'.cache-{user_id}'

    # Create a new Spotipy instance with the cache path
    sp = create_spotify_instance(cache_path)
    
    # Retrieve the access token from the URL query parameters
    code = request.args.get('code')
    sp.auth_manager.get_access_token(code)
    
    cache_file = open(cache_path, "r")
    str_cache = str(cache_file.read())

    update_user = User(id=user_id, cache=str_cache)
    
    try:
        db.session.update(update_user)
        db.session.commit()
    except:
        print("failed")
    
    # response = {'success': True, 'message': 'Spotify Linking Successful'}
    # return jsonify(response)
    # Redirect the user to the homepage
    return redirect('/spotify_recommendation')

# Endpoint for getting Spotify recommendations for the authenticated user
@spotify_login.route('/spotify_recommendation', methods=['GET'])
def recommendations():

    print('Recommendations endpoint')
    # Get the cache path for this user
    user_id = session.get('user_id')
    cache_path = f'.cache-{user_id}'

    # Create a new Spotipy instance with the cache path
    sp = create_spotify_instance(cache_path)
    user = sp.current_user()['id']

    print('Spotify User ID', user)

    track_uris = []
    track_names = []
    track_artists = []
    # track_genres = []

    ct = 1
    max_songs = 100
    
    # GET LISTENING HISTORY

    # Get the user's recently played tracks
    results = sp.current_user_recently_played(limit=50)

    print('Recently Played')

    # Print the track details
    for item in results['items']:
        track = item['track']
        track_uri = track['uri']
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        # track_genre = sp.artist(sp.track(track_uri.split(':')[-1])['artists'][0]['id'])['genres']

        track_uris.append(track_uri)
        track_names.append(track_name)
        track_artists.append(track_artist)
        # track_genres.append(track_genres)
        
        print(ct, track_uri, track_name, track_artist)
        ct += 1

    print('Recommendation by top artists')

    if len(track_uris) < max_songs:

        # Get the user's top artists
        top_artists = sp.current_user_top_artists(time_range='long_term', limit=20) # short_term, medium_term, long_term
        
        # Get recommendations based on the user's top artists
        artist_ids = [artist['id'] for artist in top_artists['items']]

        while len(artist_ids) > 0 and len(track_uris) < max_songs:
            i = artist_ids.pop(0)
                
            limit = 5
            if (max_songs - len(track_uris)) < 5:
                limit = max_songs - len(track_uris)

            recommendations = sp.recommendations([i],limit=limit)
            # print(recommendations)
            for track in recommendations['tracks']:
                track_uri = track['uri']
                track_name = track['name']
                track_artist = track['artists'][0]['name']
                # track_genres = sp.artist(sp.track(track_uri.split(':')[-1])['artists'][0]['id'])['genres']
                
                track_uris.append(track_uri)
                track_names.append(track_name)
                track_artists.append(track_artist)
                # track_genres.append(track_genres)
                
                print(ct, track_uri, track_name, track_artist)
                ct += 1

    print('Generic Recommendation')

    if len(track_uris) < max_songs:
        # Set seed attributes for the recommendation
        seed_artists = None
        seed_genres = ['pop', 'hip-hop', 'rock', 'indie', 'edm']
        seed_tracks = None
        limit = max_songs - len(track_uris)
        # Get track recommendations based on seed attributes
        recommendations = sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit=limit)

        for track in recommendations['tracks']:
                track_uri = track['uri']
                track_name = track['name']
                track_artist = track['artists'][0]['name']
                # track_genres = sp.artist(sp.track(track_uri.split(':')[-1])['artists'][0]['id'])['genres']
                
                track_uris.append(track_uri)
                track_names.append(track_name)
                track_artists.append(track_artist)
                # track_genres.append(track_genres)
                
                print(ct, track_uri, track_name, track_artist)
                ct += 1
    
    try:
        tracks_db_entry(track_uris, track_names, track_artists, cache_path)
    except Exception as e:
        print(e)
    
    response = {'success': True, 'message': 'Spotify Linking Successful'}
    return jsonify(response)
    # return f"<h1>Spotify Recommendations</h1><h3>{user}<h3><ul><li>{'</li><li>'.join(track_names)}</li></ul>"

def tracks_db_entry(track_uris, track_names, track_artists, cache_path):
    print('Inside tracks_db_entry')

    for i in range(len(track_uris)):

        track_uri = track_uris[i]
        track_name = track_names[i]
        track_artist = track_artists[i]
        
        # add entry in tracks table
        trk = Tracks.query.filter_by(track_uri=track_uri).first()
        
        if trk is None:
            new_track = Tracks(track_uri=track_uri, track_name=track_name, track_artist=track_artist)
            
            try:
                db.session.add(new_track)
                db.session.commit()
                track_id = new_track.id
            except Exception as e:
                print(e)
                db.session.rollback()
                response = {'success': False, 'message': 'Error adding track.', 'data' : track_uri}
                print(response)
                return jsonify(response)

        else:
            track_id = trk.id
        
        print('track_id', track_id)

        # add entry in usertracks table
        
        user_id=session.get('user_id')
        new_user_track = UserTracks(user_id=user_id, track_id=track_id)
        
        try:
            db.session.add(new_user_track)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            response = {'success': False, 'message': 'Error adding track in usertracks table.', 'data' : '{track_id} {user_id}'}
            print(response)
            return jsonify(response)

    response = {'success': True, 'message': 'Tracks added successfully.'}
    os.remove(cache_path)
    return jsonify(response)

#-----------------------------------------------

# CREATE PLAYLIST USING RECOMMENDED SONGS

# playlist_name = 'Trial Playlist'
# playlist_description = 'Playlist of recommended songs from SpotiFyre App'
# playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=playlist_name, public=False, collaborative=True, description=playlist_description)

# # Get the list of recommended tracks
# tracks = [track['uri'] for track in recommendations['tracks']]

# # Add the recommended tracks to the new playlist
# sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlist['id'], tracks=tracks[:100])

#-----------------------------------------------

# GET RECOMMENDED SONGS BY TOP ARTISTS AND GENRES

# recommendations = sp.recommendations(seed_artists=[artist['id'] for artist in top_artists['items']], seed_genres=[preferred_genre], limit=20)

#-----------------------------------------------

# GET LISTENING HISTORY

# # Get the user's recently played tracks
# results = sp.current_user_recently_played(limit=50)

# # Print the track details
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")

