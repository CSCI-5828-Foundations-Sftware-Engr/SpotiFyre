import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, redirect

app = Flask(__name__)

# Set up the Spotify API credentials
client_id = '3d7af19cb8f84dcab05b9f44feab935e'
client_secret = 'e21a86202bc14a83a20f32c80e0d700b'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative'

# auth_manager = SpotifyOAuth(client_id, client_secret, redirect_uri, scope)

print(client_id, client_secret, redirect_uri)

# Create a Spotipy instance with a new cache path for each user
def create_spotify_instance(cache_path):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                      client_secret=client_secret,
                                                      redirect_uri=redirect_uri,
                                                      scope=scope,
                                                      cache_path=cache_path))

# Endpoint for initiating the Spotify authentication flow
@app.route('/login')
def login():
    print('Login endpoint')
    # Get the cache path for this user
    cache_path = f'.cache-{request.remote_addr}'
    
    # Create a new Spotipy instance with the cache path
    sp = create_spotify_instance(cache_path)
    
    # Redirect the user to the Spotify login page
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

# Endpoint for retrieving the access token after the user has logged in
@app.route('/callback')
def callback():
    print('callback endpoint')
    # Get the cache path for this user
    cache_path = f'.cache-{request.remote_addr}'
    
    # Create a new Spotipy instance with the cache path
    sp = create_spotify_instance(cache_path)
    
    # Retrieve the access token from the URL query parameters
    code = request.args.get('code')
    sp.auth_manager.get_access_token(code)
    
    # Redirect the user to the homepage
    return redirect('/')

# Endpoint for getting Spotify recommendations for the authenticated user
@app.route('/')
def recommendations():

    print('Recommendations endpoint')
    # Get the cache path for this user
    cache_path = f'.cache-{request.remote_addr}'
    
    # Create a new Spotipy instance with the cache path
    sp = create_spotify_instance(cache_path)
    
    # Get the user's top artists
    top_artists = sp.current_user_top_artists(time_range='long_term', limit=10) # short_term, medium_term, long_term
    
    # Get recommendations based on the user's top artists
    seed_artists=[artist['id'] for artist in top_artists['items']]

    track_uris = []
    track_names = []
    
    for i in seed_artists:
        # print(i)
        recommendations = sp.recommendations([i],limit=20)
        track_uris += [track['uri'] for track in recommendations['tracks']]
        track_names += [f"{t['name']} by {t['artists'][0]['name']}" for t in recommendations['tracks']] # to get names of songs from the recommendations
    
    return f"<h1>Spotify Recommendations</h1><ul><li>{'</li><li>'.join(track_names)}</li></ul>"

if __name__ == '__main__':
    app.run()

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

# SHARE PLAYLIST WITH OTHER USERS

# collaborators = ["31sxvmqfalwsyg232ldxxevwqaqy"]
# for user in collaborators:
#     sp.user_playlist_change_details(user=user, playlist_id=playlist["id"], collaborative=True)
#     sp.user_playlist_follow_playlist(user, playlist_id=playlist['id'])