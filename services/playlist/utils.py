from sqlalchemy import select, update
from models import User, Group, Tracks, UserTracks, Playlists, Member
from sqlalchemy.orm import sessionmaker
from session import session

import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
scope = os.getenv('SPOTIFY_SCOPE')

# Create a Spotipy instance with a new cache path for each user
def create_spotify_instance(cache_path):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                      client_secret=client_secret,
                                                      redirect_uri=redirect_uri,
                                                      scope=scope,
                                                      cache_path=cache_path))

def get_group_by_id(group_id):
    group = session.query(Group).filter_by(id = group_id).first()

    if group is not None:
        # for member in group.members:
        #     print(member.name)
        print("group found", group)
        return group
    else:
        return None

def get_group_members(group):
    members = session.query(Member).join(User, onclause=Member.user_id==User.id).filter(Member.group_id == group.id).all()

    return members


def get_all_tracks(members, num_tracks):
    # Get list of user_ids of all group members
    if members:
        member_ids = [member.user_id for member in members]
        print("member_ids", member_ids)
    # Get all distinct tracks for all member ids
        all_tracks = session.query(UserTracks.user_id, UserTracks.track_id) \
                        .join(Tracks, UserTracks.track_id == Tracks.id) \
                        .filter(UserTracks.user_id.in_(member_ids)).all()
                        # .group_by(UserTracks.user_id)
        
        track_ids = set()

        for track in all_tracks:
            track_ids.add(track.track_id)
        
        # Create dict of user to list of tracks
        user_tracks = list(track_ids)

        pl_tracks = session.query(Tracks).filter(Tracks.id.in_(user_tracks)).all()

        return pl_tracks
    else:
        print("No group found")


def get_playlist_tracks(pl_tracks, num_tracks):

    pl_track_uris = list() # [track for track in all_tracks]
    counter = 0
    for track in pl_tracks:
        if counter < num_tracks:
            pl_track_uris.append(track.track_uri)
        counter += 1
    
    return pl_track_uris

def create_spotify_playlist(user_id, playlist_id, name):
    user = session.query(User).filter_by(id=user_id).first()
    cache_path = f"cache_{user.id}"
    f = open(cache_path, "w")
    f.write(user.cache)
    f.close()

    sp = create_spotify_instance(cache_path)
    spotify_user_id = sp.current_user()['id']
    new_playlist = sp.user_playlist_create(user=spotify_user_id, name=name, public=True, collaborative=False, description="Enjoy!")

    playlist_url = new_playlist['external_urls']['spotify']

    session.query(Playlists).filter(Playlists.id == playlist_id).update({'link': playlist_url})
    
    session.commit()

    return new_playlist


def add_tracks(user_id, tracks, playlist):
    user = session.query(User).filter_by(id=user_id).first()
    cache_path = f"cache_{user.id}"
    f = open(cache_path, "w")
    f.write(user.cache)
    f.close()

    sp = create_spotify_instance(cache_path)
    spotify_user_id = sp.current_user()['id']

    add_tracks_req = sp.user_playlist_add_tracks(user=spotify_user_id, playlist_id=playlist['id'], tracks=tracks)

    return add_tracks_req


def create_playlist(playlist_data):
    # 1. Get group members from playlist_data.group_id
    pl_data = json.loads(playlist_data)
    group = get_group_by_id(pl_data["group_id"])

    members = get_group_members(group)
    # 2. Get tracks of each member of group
    all_tracks = get_all_tracks(members, pl_data["num_tracks"])
    print(all_tracks)
    # 3. Create a list of tracks of length playlist_data.num_tracks from all the tracks for each member
    playlist_tracks = get_playlist_tracks(all_tracks, pl_data["num_tracks"])

    # 4. Create playlist (empty initially)
    #   a. ENDPOINT:  https://api.spotify.com/v1/users/{user_id}/playlists
    #   b. Req body: name, description, public
    #   c. Response will contain {
    #     "external_urls": {
    #         "spotify": "string"
    #     },
    #     "href": "string",
    #     "id": "string",
    #     "name": "string",
    #     "type": "string",
    #     "uri": "string"
    #     }
    create_resp = create_spotify_playlist(group.owner_id, pl_data["id"], pl_data["playlist_name"])

    print(create_resp)

    add_resp = add_tracks(group.owner_id, playlist_tracks, create_resp)

    print(add_resp)
    
    # 5. Add 3. to 4.
    #   a. ENDPOINT:  https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    #   b. Req body: {"uris": ["string"],"position": 0}
    #   c. Response: {"snapshot_id": "abc"}
    
    
    # 6. Update playlist_data.link with the playlist.external_urls.spotify url string.
    
    
    # 7. return success


    # group_id, id, playlist_name, num_tracks