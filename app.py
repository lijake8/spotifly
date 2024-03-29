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

SCOPES_LIST = ['user-read-currently-playing', 'playlist-modify-private', 'playlist-read-private', 'playlist-read-collaborative', 'user-library-read', 'user-library-modify']
SCOPES_STR = ' '.join(SCOPES_LIST)
SCOPES_URL = '+'.join(SCOPES_LIST)

def get_auth_header(token):
	return {
		"Authorization": f"Bearer {token}"
	}

def setup_api_client():
	cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
	auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
																							client_secret=CLIENT_SECRET,
																							redirect_uri=REDIRECT_URI,
																							cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
			return redirect('/')
	return spotipy.Spotify(auth_manager=auth_manager)

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

		# get liked songs and save to session
		track_results = spotify.current_user_saved_tracks(limit=50, offset=0)
		tracks = track_results['items']
		while track_results['next']:
				track_results = spotify.next(track_results)
				tracks.extend(track_results['items'])
		liked_songs = [track['track'] for track in tracks if track['track']['preview_url'] is not None]

		#add audio features to each liked song, 100 at a time
		liked_song_ids = [song['id'] for song in liked_songs]
		liked_song_features = []
		for i in range(0, len(liked_song_ids), 100):
				liked_song_features.extend(spotify.audio_features(liked_song_ids[i:i+100]))
		for i in range(len(liked_songs)):
				liked_songs[i]['audio_features'] = liked_song_features[i]


		session['liked_songs'] = liked_songs
		print('example tempo', liked_songs[0]['audio_features']['tempo'])



		# cache saved (liked) tracks for each artist
		# from liked songs, make a map of (artist id: [{track id, track name, track preview url, track image url}, ]) 
		artist_track_map = {}
		for track in tracks:
			artist_id = track['track']['artists'][0]['id']
			if artist_id in artist_track_map:
				artist_track_map[artist_id].append({
					'id': track['track']['id'],
					'name': track['track']['name'],
					'preview_url': track['track']['preview_url'],
					'album_image_url': track['track']['album']['images'][0]['url'] if len(track['track']['album']['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png'
				})
			else:
				artist_track_map[artist_id] = [{
					'id': track['track']['id'],
					'name': track['track']['name'],
					'preview_url': track['track']['preview_url'],
					'album_image_url': track['track']['album']['images'][0]['url'] if len(track['track']['album']['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png'
				}]
		session['artist_track_map'] = artist_track_map

		# map of artist id to artist info to load that artist's page faster
		session['artist_info'] = {}


		return render_template('user.html', user=user)
	

@app.route('/sign_out')
def sign_out():
		session.pop("token_info", None)
		return redirect('/')


@app.route('/playlists')
def playlists():
		spotify = setup_api_client()
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
		spotify = setup_api_client()
		track = spotify.current_user_playing_track()
		if not track is None:
				return track
		return "No track currently playing."


@app.route('/current_user')
def current_user():
	spotify = setup_api_client()
	return spotify.me()


@app.route('/hover-test')
def hover_test():
	items = [{'title': 'blah1', 'description': 'blahblah1'}, {'title': 'blah2', 'description': 'blahblah2'}, {'title': 'blah3', 'description': 'blahblah3'}, {'title': 'blah4', 'description': 'blahblah4'}]
	items1 = [{'title': 'bruh1', 'description': 'bruhbruh1'}, {'title': 'bruh2', 'description': 'bruhbruh2'}, {'title': 'bruh3', 'description': 'bruhbruh3'}, {'title': 'bruh4', 'description': 'bruhbruh4'}, {'title': 'bruh5', 'description': 'bruhbruh5'}]
	items2 = [{'title': 'dawg1', 'description': 'dawgdawg1'}, {'title': 'dawg2', 'description': 'dawgdawg2'}, {'title': 'dawg3', 'description': 'dawgdawg3'}, {'title': 'dawg4', 'description': 'dawgdawg4'}, {'title': 'dawg5', 'description': 'dawgdawg5'}, {'title': 'dawg6', 'description': 'dawgdawg6'}]
	return render_template('hover-test.html', items=items, items1=items1, items2=items2)



@app.route('/song-view/<track_id>')
def song_view(track_id):
	spotify = setup_api_client()

	track = spotify.track(track_id)
	features = spotify.audio_features([track_id])
	return {
		'features': features, 
		'track': track
	}

@app.route('/album-view/<album_id>')
def album_view(album_id):
	spotify = setup_api_client()

	album = spotify.album(album_id)
	tracks = spotify.album_tracks(album_id)
	# return {
	# 	'album': album, 
	# 	'tracks': tracks
	# }
	return render_template('album.html', album=album, tracks=tracks)


# @app.route('/playlist-view')
@app.route('/playlist-view/<playlist_id>')
def playlist_view(playlist_id):
	spotify = setup_api_client()

	playlist = spotify.playlist(playlist_id)
	tracks = playlist['tracks']['items']
	while playlist['tracks']['next']:
			playlist['tracks'] = spotify.next(playlist['tracks'])
			tracks.extend(playlist['tracks']['items'])

	# remove local file tracks because they have no preview
	for track in tracks:
		if track['track']['is_local']:
			tracks.remove(track)
	
	return render_template('playlist.html', playlist=playlist, tracks=tracks)


@app.route('/my-songs')
def my_songs():
	# get liked songs from session
	liked_songs = session.get('liked_songs', [])
	return liked_songs




@app.route('/artist-view/<artist_id>')
def artist_view(artist_id):
	if artist_id in session['artist_info']:
		artist_info = session['artist_info'][artist_id]
		return render_template('artist.html', artist_image_url=artist_info['artist_image_url'], artist_name=artist_info['artist_name'], followers=artist_info['followers'], album_info=artist_info['album_info'], liked_tracks=artist_info['liked_tracks'], top_tracks=artist_info['top_tracks'], single_info=artist_info['single_info'], compilation_info=artist_info['compilation_info'])
	else:
		spotify = setup_api_client()

		artist = spotify.artist(artist_id)
		followers_str = str(round(artist['followers']['total']/1000000, 1)) + 'M' if artist['followers']['total'] > 1000000 else str(round(artist['followers']['total']/1000, 1)) + 'K' if artist['followers']['total'] > 1000 else '<1K'
		artist_image_url = artist['images'][0]['url'] if len(artist['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png'
		artist_name = artist['name']

		albums = spotify.artist_albums(artist_id, limit=50)
		album_list = albums['items'] #list of SimplifiedAlbumObjects
		while albums['next']:
				albums = spotify.next(albums)
				album_list.extend(albums['items'])

		# if album is not primarily by this artist, ignore it
		album_list = [album for album in album_list if album['artists'][0]['id'] == artist_id]

		album_ids = [album['id'] for album in album_list] #get album ids to get tracks
		
		# get detailed album info from albums 20 at a time
		detailed_albums = [] # list of AlbumObjects
		for i in range(0, len(album_ids), 20):
				detailed_albums.extend(spotify.albums(album_ids[i:i+20])['albums'])

			
		
		album_info = {} # map of album id: {album image url:, album name:, album release date:, album total tracks:, popularity:, year:, tracks: [{name:, preview url:, id:}, ...]}
		single_info = {}
		compilation_info = {}
		for album in detailed_albums:
			if album['album_type'] == 'single':
				single_info[album['id']] = {
					'album_image_url': album['images'][0]['url'] if len(album['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png',
					'album_name': album['name'],
					'album_release_date': album['release_date'],
					'album_total_tracks': album['total_tracks'],
					'popularity': album['popularity'],
					'year': album['release_date'][:4], #first 4 chars of release date is the year
					'tracks': []
				}
				for track in album['tracks']['items']:
					single_info[album['id']]['tracks'].append({
						'name': track['name'],
						'preview_url': track['preview_url'],
						'id': track['id']
					})
			elif album['album_type'] == 'compilation':
				compilation_info[album['id']] = {
					'album_image_url': album['images'][0]['url'] if len(album['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png',
					'album_name': album['name'],
					'album_release_date': album['release_date'],
					'album_total_tracks': album['total_tracks'],
					'popularity': album['popularity'],
					'year': album['release_date'][:4], #first 4 chars of release date is the year
					'tracks': []
				}
				for track in album['tracks']['items']:
					compilation_info[album['id']]['tracks'].append({
						'name': track['name'],
						'preview_url': track['preview_url'],
						'id': track['id']
					})
			else:
				album_info[album['id']] = {
					'album_image_url': album['images'][0]['url'] if len(album['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png',
					'album_name': album['name'],
					'album_release_date': album['release_date'],
					'album_total_tracks': album['total_tracks'],
					'popularity': album['popularity'],
					'year': album['release_date'][:4], #first 4 chars of release date is the year
					'tracks': []
				}
				for track in album['tracks']['items']:
					album_info[album['id']]['tracks'].append({
						'name': track['name'],
						'preview_url': track['preview_url'],
						'id': track['id']
					})
			
		# get user liked songs for this artist
		if artist_id in session['artist_track_map']:
			liked_tracks = session['artist_track_map'][artist_id]

		# get top tracks for this artist
		top_tracks_res = spotify.artist_top_tracks(artist_id)['tracks']
		print('top tracks', top_tracks_res)
		top_tracks = []
		for track in top_tracks_res:
			top_tracks.append({
				'name': track['name'],
				'preview_url': track['preview_url'],
				'id': track['id'],
				'album_image_url': track['album']['images'][0]['url'] if len(track['album']['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png'
			})

		artist_info = {
			'artist_image_url': artist_image_url,
			'artist_name': artist_name,
			'followers': followers_str,
			'album_info': album_info,
			'liked_tracks': liked_tracks,
			'top_tracks': top_tracks,
			'single_info': single_info,
			'compilation_info': compilation_info
		}
		session['artist_info'][artist_id] = artist_info
		
		# with open('mocking_dummy.json', 'w') as f:
		# 	json.dump(artist_info, f)
		return render_template('artist.html', artist_image_url=artist_image_url, artist_name=artist_name, followers=followers_str, album_info=album_info, liked_tracks=liked_tracks, top_tracks=top_tracks, single_info=single_info, compilation_info=compilation_info)
	


	# with open('session_liked_songs.json', 'w') as f1:
	# 	json.dump(session['artist_track_map'], f1)

	# for mocking without repeating api calls
	# with open('mocking_dummy.json', 'r') as f:
	# 	mocking_dummy = json.load(f)
	# return render_template('artist.html', artist_image_url=mocking_dummy['artist_image_url'], artist_name=mocking_dummy['artist_name'], followers=mocking_dummy['followers'], album_info=mocking_dummy['album_info'], liked_tracks=mocking_dummy['liked_tracks'], top_tracks=mocking_dummy['top_tracks'], single_info=mocking_dummy['single_info'], compilation_info=mocking_dummy['compilation_info'])


@app.route('/search/<query>')
def search(query):
	"""Search for tracks, albums, artists, playlists matching a search query"""

	spotify = setup_api_client()

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

	spotify = setup_api_client()

	track = spotify.track(track_id)
	recommendations = spotify.recommendations(seed_tracks=[track_id], limit=100)
	return {
		'original_track': track,
		'recommendations': recommendations['tracks']
	}


@app.route('/recommendation-sandbox', methods=["GET", "POST"])
def recommendation_sandbox():
	"""Get recommendations based on song characteristics"""

	#TODO: fix bug where sliders are reset after submitting form

	def concatenate_slider_values(slider_values):
		"""serverside method to concatenate, causes page reload"""
		result = ""
		for value in slider_values:
				result += str(value)
		return result

	if request.method == "POST":
		slider_values = [int(request.form["slider1"]), int(request.form["slider2"]), int(request.form["slider3"])]

		# Run the Python function to concatenate the slider values
		result = 'backend result: ' + concatenate_slider_values(slider_values)

		# Display the result below the button
		return render_template("recommendation-sandbox.html", result=result)

	return render_template("recommendation-sandbox.html")


@app.route('/concatenate', methods=['GET', 'POST'])
def concatenate():
		"""clientside method to concatenate, dynamic page update without reload"""
		if request.method == 'GET':
				return render_template("concatenate.html")
		if request.method == 'POST':
				slider1 = request.form.get('slider1')
				slider2 = request.form.get('slider2')
				slider3 = request.form.get('slider3')
				concatenated = str(slider1) + str(slider2) + str(slider3)
				return concatenated



@app.route('/error')
@app.route('/page-not-found')
def error():
		raise Exception("Error!")
		return render_template("error.html")


@app.route('/test-visualizer')
def test_visualizer():
		return render_template("test-visualizer.html")

@app.route('/test-autoplay')
def test_autoplay():
		song_urls = [
        'https://p.scdn.co/mp3-preview/4d9bde799eec8913e53c184c45b9fd575690b917?cid=9688e06282ff4043a95d46dee1f7467d',
        'https://p.scdn.co/mp3-preview/337c8d45ac66899bc2db9ef3ed9438fe1d035ab1?cid=9688e06282ff4043a95d46dee1f7467d',
        'https://p.scdn.co/mp3-preview/547de9accd9a23cb808f2497c5512151ed12baa4?cid=9688e06282ff4043a95d46dee1f7467d'
    ]
		data = {'song_urls': song_urls}
		return render_template("test-autoplay.html", data=data)

@app.route('/play/<type>/<data>')
def play(type, data):
		#use cases
		#play all artist songs 
		#play top songs from artist
		#play liked songs from artist
		#play specific playlist
		#play album
		#play user liked songs
		#play generated playlist from recommendation sandbox

		#type can be 'album' (includes singles), 'playlist', 'artist', 'liked', etc TBD


		if type == 'liked':
				if data == 'all':
						#play all liked songs

						
						#for mocking
						# liked_tracks = [
						# 	{'name': 'song1', 'audio_url': '/static/cropped-audio-samples/1.mp3', 'genre': 'pop'},
						# 	{'name': 'song2', 'audio_url': '/static/cropped-audio-samples/2.mp3', 'genre': 'electronic'},
						# 	{'name': 'song3', 'audio_url': '/static/cropped-audio-samples/3.mp3', 'genre': 'pop'},
						# 	{'name': 'song4', 'audio_url': '/static/cropped-audio-samples/4.mp3', 'genre': 'rock'},
						# 	{'name': 'song5', 'audio_url': '/static/cropped-audio-samples/5.mp3', 'genre': 'rock'},
						# 	{'name': 'song6', 'audio_url': '/static/cropped-audio-samples/6.mp3', 'genre': 'rock'},
						# ]

						#test: get only tracks 115-130 bpm with high energy and danceability
						tempo_min = 100
						tempo_max = 180
						energy_min = 0.8
						danceability_min = 0.6


						liked_tracks = []
						for song in session['liked_songs']:
								if song['audio_features']['tempo'] >= tempo_min and song['audio_features']['tempo'] <= tempo_max and song['audio_features']['energy'] >= energy_min and song['audio_features']['danceability'] >= danceability_min:
										liked_tracks.append({
												'name': song['name'],
												'artist': song['artists'][0]['name'], #TODO: handle multiple artists
												'preview_url': song['preview_url'],
												'image': song['album']['images'][0]['url'] if len(song['album']['images']) > 0 else 'https://www.freeiconspng.com/uploads/spotify-icon-2.png'
										})
								
						
						#shuffle liked_tracks
						import random
						random.shuffle(liked_tracks)

						print('og liked tracks length', len(session['liked_songs']))
						print('liked tracks length after filtering for danceability, energy, tempo', len(liked_tracks))


						return render_template("player.html", liked_tracks=json.dumps(liked_tracks), test=[{'test': 'test'}])
						# return session['liked_songs']
				
		return {}


# In[4]: run app
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)