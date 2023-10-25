from flask import Flask, render_template, session, request, redirect
import os
from flask_session import Session
import spotipy
from dotenv import load_dotenv
import requests
import json

# In[0]: allow api keys to be pulled from .env environment file
load_dotenv()

# In[1]: set up flask app and session
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64) #sets the secret key for the Flask application. The secret key is used to encrypt session cookies and other sensitive data
app.config['SESSION_TYPE'] = 'filesystem' #sets the session type for the Flask application to be stored on the file system. By default, Flask uses a client-side session, but here it is configured to use server-side sessions stored on the file system. https://stackoverflow.com/questions/68902836/what-is-the-difference-between-client-side-based-sessions-and-server-side-sessio
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

# In[2]: globals
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

SCOPES_LIST = ['user-read-currently-playing', 'playlist-modify-private']
SCOPES_STR = ' '.join(SCOPES_LIST)
SCOPES_URL = '+'.join(SCOPES_LIST)

def get_auth_header(token):
	return {
		"Authorization": f"Bearer {token}"
	}

# In[3]: routes
@app.route("/")
@app.route("/index")
def index():
		#store the token info in the session framework provided by flask; then create a SpotifyOAuth object
		cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session) 
		auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
													client_secret=CLIENT_SECRET,
													redirect_uri=REDIRECT_URI,
													scope=SCOPES_STR,
													cache_handler=cache_handler,
													show_dialog=True)

		if request.args.get("code"): #access parameter '?code=' in the URL
			# Step 2. Being redirected from Spotify auth page
			auth_manager.get_access_token(request.args.get("code"))
			return redirect('/')

		if not auth_manager.validate_token(cache_handler.get_cached_token()):
			# Step 1. Display spotify sign in page when no token
			auth_url = auth_manager.get_authorize_url()
			return render_template("login.html", auth_url=auth_url)

		# Step 3. Signed in, display data
		spotify = spotipy.Spotify(auth_manager=auth_manager)
		user = spotify.me()
		return render_template('user.html', user=user)
	

@app.route('/sign_out')
def sign_out():
		session.pop("token_info", None)
		return redirect('/')


@app.route('/playlists')
def playlists():
		cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
		auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI, 
																							 cache_handler=cache_handler)
		if not auth_manager.validate_token(cache_handler.get_cached_token()):
				return redirect('/')

		spotify = spotipy.Spotify(auth_manager=auth_manager)
		#loop thru to get all the playlists because the limit is 50 at a time
		results = spotify.current_user_playlists(limit=50, offset=0)
		playlists = results['items']
		while results['next']:
				results = spotify.next(results)
				playlists.extend(results['items'])

		print(len(playlists))
		print(json.dumps(playlists[0]))
		
		return render_template('my-playlists.html', playlists=playlists)


@app.route('/currently_playing')
def currently_playing():
		cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
		auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI,
																							 cache_handler=cache_handler)
		if not auth_manager.validate_token(cache_handler.get_cached_token()):
				return redirect('/')
		spotify = spotipy.Spotify(auth_manager=auth_manager)
		track = spotify.current_user_playing_track()
		if not track is None:
				return track
		return "No track currently playing."


@app.route('/current_user')
def current_user():
	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
												 client_secret=CLIENT_SECRET,
												 redirect_uri=REDIRECT_URI,
												 cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)
	return spotify.me()


@app.route('/hover-test')
def hover_test():
	items = [{'title': 'blah1', 'description': 'blahblah1'}, {'title': 'blah2', 'description': 'blahblah2'}, {'title': 'blah3', 'description': 'blahblah3'}, {'title': 'blah4', 'description': 'blahblah4'}]
	items1 = [{'title': 'bruh1', 'description': 'bruhbruh1'}, {'title': 'bruh2', 'description': 'bruhbruh2'}, {'title': 'bruh3', 'description': 'bruhbruh3'}, {'title': 'bruh4', 'description': 'bruhbruh4'}, {'title': 'bruh5', 'description': 'bruhbruh5'}]
	items2 = [{'title': 'dawg1', 'description': 'dawgdawg1'}, {'title': 'dawg2', 'description': 'dawgdawg2'}, {'title': 'dawg3', 'description': 'dawgdawg3'}, {'title': 'dawg4', 'description': 'dawgdawg4'}, {'title': 'dawg5', 'description': 'dawgdawg5'}, {'title': 'dawg6', 'description': 'dawgdawg6'}]
	return render_template('hover-test.html', items=items, items1=items1, items2=items2)



@app.route('/song-view/<track_id>')
def song_view(track_id):
	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI, 
																							 cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)

	track = spotify.track(track_id)
	features = spotify.audio_features([track_id])
	return {
		'features': features, 
		'track': track
	}

@app.route('/album-view/<album_id>')
def album_view(album_id):
	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI, 
																							 cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)

	album = spotify.album(album_id)
	tracks = spotify.album_tracks(album_id)
	return {
		'album': album, 
		'tracks': tracks
	}

# @app.route('/playlist-view')
@app.route('/playlist-view/<playlist_id>')
def playlist_view(playlist_id):
	
	# NATIVE API WAY
	# headers = get_auth_header(session['token_info']['access_token'])
	# playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
	# response = requests.get(playlist_url, headers=headers)
	# playlist_items = response.json()['items']
	# # print(json.dumps(playlist_items[0])) #single song in playlist
	# print('NATIVE TOKEN', session['token_info']['access_token'])


	# SPOTIPY WAY
	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							client_secret=CLIENT_SECRET,
																							redirect_uri=REDIRECT_URI, 
																							cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)
	playlist = spotify.playlist(playlist_id)
	# print('AUTH MANAGER TOKEN', auth_manager.get_access_token()) #session['token_info']['access_token']
	# print('AUTH MANAGER TOKEN', auth_manager.get_cached_token())
	# auth_manager.refresh_access_token(auth_manager.get_cached_token()['refresh_token'])

	tracks = playlist['tracks']['items']
	while playlist['tracks']['next']:
			playlist['tracks'] = spotify.next(playlist['tracks'])
			tracks.extend(playlist['tracks']['items'])

	# print(playlist)
	print('tracks in playlist:', len(tracks))
	return [(track['track']['name'], track['track']['preview_url']) for track in tracks]


@app.route('/artist-view/<artist_id>')
def artist_view(artist_id):
	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI, 
																							 cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)

	artist = spotify.artist(artist_id)
	albums = spotify.artist_albums(artist_id)
	return {
		'artist': artist, 
		'albums': [album['name'] for album in albums['items']]
	}


@app.route('/search/<query>')
def search(query):
	"""Search for tracks, albums, artists, playlists matching a search query"""

	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI, 
																							 cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)

	#search tracks, albums, artists, playlists
	track_results = spotify.search(query, limit=10)
	album_results = spotify.search(query, type='album', limit=10)
	artist_results = spotify.search(query, type='artist', limit=10)
	playlist_results = spotify.search(query, type='playlist', limit=10)

	return {
		'tracks': track_results['tracks']['items'],
		'albums': album_results['albums']['items'],
		'artists': artist_results['artists']['items'],
		'playlists': playlist_results['playlists']['items']
	}

#TODO: possibly just make this a func to call on the page and not a route, have a route for creating and saving a playlist based on recommnedations
@app.route('/recommendations/<track_id>')
def recommendations(track_id):
	"""Get recommendations based on a track"""

	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							 client_secret=CLIENT_SECRET,
																							 redirect_uri=REDIRECT_URI, 
																							 cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	spotify = spotipy.Spotify(auth_manager=auth_manager)

	track = spotify.track(track_id)
	recommendations = spotify.recommendations(seed_tracks=[track_id], limit=100)
	return {
		'original_track': track,
		'recommendations': recommendations['tracks']
	}


@app.route('/recommendation-sandbox', methods=["GET", "POST"])
def recommendation_sandbox():
	"""Get recommendations based on song characteristics"""

	def concatenate_slider_values(slider_values):
		"""Concatenates the slider values as strings and returns the result."""
		result = ""
		for value in slider_values:
				result += str(value)
		return result

	if request.method == "POST":
		slider_values = [int(request.form["slider1"]), int(request.form["slider2"]), int(request.form["slider3"])]

		# Run the Python function to concatenate the slider values
		result = concatenate_slider_values(slider_values)

		# Display the result below the button
		return render_template("recommendation-sandbox.html", result=result)

	return render_template("recommendation-sandbox.html")


@app.route('/concatenate', methods=['GET', 'POST'])
def concatenate():
		if request.method == 'GET':
				return render_template("concatenate.html")
		if request.method == 'POST':
				slider1 = request.form.get('slider1')
				slider2 = request.form.get('slider2')
				slider3 = request.form.get('slider3')
				concatenated = str(slider1) + str(slider2) + str(slider3)
				return concatenated


# In[4]: run app
if __name__ == '__main__':
	app.run(debug=True)