from flask import Flask, render_template, session, request, redirect
import os
from flask_session import Session
import spotipy
from dotenv import load_dotenv

# In[0]: allow api keys to be pulled from .env file
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
    return spotify.current_user_playlists()


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


@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/test2')
def test2():
	items = [{'title': 'blah1', 'description': 'blahblah1'}, {'title': 'blah2', 'description': 'blahblah2'}, {'title': 'blah3', 'description': 'blahblah3'}, {'title': 'blah4', 'description': 'blahblah4'}]
	items1 = [{'title': 'bruh1', 'description': 'bruhbruh1'}, {'title': 'bruh2', 'description': 'bruhbruh2'}, {'title': 'bruh3', 'description': 'bruhbruh3'}, {'title': 'bruh4', 'description': 'bruhbruh4'}, {'title': 'bruh5', 'description': 'bruhbruh5'}]
	items2 = [{'title': 'dawg1', 'description': 'dawgdawg1'}, {'title': 'dawg2', 'description': 'dawgdawg2'}, {'title': 'dawg3', 'description': 'dawgdawg3'}, {'title': 'dawg4', 'description': 'dawgdawg4'}, {'title': 'dawg5', 'description': 'dawgdawg5'}, {'title': 'dawg6', 'description': 'dawgdawg6'}]
	return render_template('test-radio.html', items=items, items1=items1, items2=items2)


@app.route('/user-view')
def user_view():
	return redirect('/')

@app.route('/song-view')
def song_view():
	return redirect('/')

@app.route('/album-view')
def album_view():
	return redirect('/')

@app.route('/playlist-view')
def playlist_view():
	return redirect('/')

@app.route('/artist-view')
def artist_view():
	return redirect('/')



# In[4]: run app
if __name__ == '__main__':
	app.run(debug=True)