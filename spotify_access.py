import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import transition_order as t_ord


'''
client_id: c788810678c0438eade887f9d17141a2
client_secret: 14e2eae10c9841a3a575a5e73e532c7f
'''

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'aithd46dhn56'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save', _external=True))


@app.route('/save')
def save():
    # Does basic authentication and gets user id
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']

    # Get list of user's playlists
    user_playlists = sp.current_user_playlists()['items']
    playlist_pick = "MJ copy"  # This holds the playlist name in which songs will be pulled from.
    pl_pick_id = None

    # Gets playlist id and checks that it exists.
    result = next((pl for pl in user_playlists if pl['name'] == playlist_pick), None)
    pl_pick_id = result['id']
    if not pl_pick_id:
        return "Entered playlist does not exist."

    # Calls method to add each song id from playlist to a list.
    # song_uris contains two items (track_id, i). The 'i' value is the song's current number in the playlist.
    # This number will be used in future steps like TSP and sorting.
    song_uris = get_playlist_tracks(sp, pl_pick_id)
    if len(song_uris) <= 0:
        return "Selected playlist is empty."

    # Pass data to rest of algorithm
    # The remainder of the algorithm until an ordered list is returned will be performed in other classes.
    # The other classes will perform the solution to the TSP along with calculating similarity scores between
    #     songs in order to determine the optimum path through the playlist.
    ordered_list = t_ord.transitions_main(sp, song_uris)

    # Create two list containing all song uri's in the playlist.
    # remove_list: will be used to remove songs from the original playlist
    # add_list: will be used to re-add songs in the specified order.
    remove_list = []
    add_list = []
    for itr, song in enumerate(song_uris):
        remove_list.append(song[0])  # Appends the track_id to remove_list
        add_list.append(song_uris[ordered_list[itr]][0])

    # Uses the remove_list list to remove all songs from the given playlist 100 items at a time.
    while len(remove_list) > 0:
        sp.playlist_remove_all_occurrences_of_items(playlist_id=pl_pick_id, items=remove_list[:100])
        remove_list = remove_list[100:]

    # Uses the add_list list to re-add all songs to the given playlist in the specified order 100 songs at a time.
    while len(add_list) > 0:
        sp.playlist_add_items(playlist_id=pl_pick_id, items=add_list[:100])
        add_list = add_list[100:]

    # Program is complete so return success
    return "SUCCESS"


# When gathering song id's from a Spotify playlist, Spotify only allows you to gather the first 100 songs.
# This method allows us to gather 100 songs at a time by calling sp.next as long as more songs exist.
# This method then creates the song_uris list
def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    song_uris = []
    for i, t in enumerate(tracks):
        song_uris.append([(t['track'])['uri'], i])

    return song_uris


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(client_id = "c788810678c0438eade887f9d17141a2",
                        client_secret = '14e2eae10c9841a3a575a5e73e532c7f',
                        redirect_uri = url_for('redirect_page', _external=True),
                        scope = 'user-library-read playlist-modify playlist-modify-private')

app.run(debug=True)
