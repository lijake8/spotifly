## to setup:
pip install -r requirements.txt
env/scripts/activate

## to run the app
https://flowbite.com/docs/getting-started/flask/
need split terminal
  python app.py
  npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch
  ^applies the input tailwind css settings to create an output css file with all the classnames

## notes
custom components in html: https://www.freecodecamp.org/news/reusable-html-components-how-to-reuse-a-header-and-footer-on-a-website/

native api way for eg playlist view
  <!-- # NATIVE API WAY
	# headers = get_auth_header(session['token_info']['access_token'])
	# playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
	# response = requests.get(playlist_url, headers=headers)
	# playlist_items = response.json()['items']
	# # print(json.dumps(playlist_items[0])) #single song in playlist
	# print('NATIVE TOKEN', session['token_info']['access_token']) 
  # print('AUTH MANAGER TOKEN', auth_manager.get_access_token()) #session['token_info']['access_token']
	# print('AUTH MANAGER TOKEN', auth_manager.get_cached_token())
	# auth_manager.refresh_access_token(auth_manager.get_cached_token()['refresh_token']) -->

## hardcodings for mocking
sample mp3 urls: 
- https://p.scdn.co/mp3-preview/4d9bde799eec8913e53c184c45b9fd575690b917?cid=9688e06282ff4043a95d46dee1f7467d
- https://p.scdn.co/mp3-preview/337c8d45ac66899bc2db9ef3ed9438fe1d035ab1?cid=9688e06282ff4043a95d46dee1f7467d
- https://p.scdn.co/mp3-preview/547de9accd9a23cb808f2497c5512151ed12baa4?cid=9688e06282ff4043a95d46dee1f7467d
- https://p.scdn.co/mp3-preview/3b01294b6b0458fea6ed5a88ea1b1593eb495ead?cid=9688e06282ff4043a95d46dee1f7467d
- https://p.scdn.co/mp3-preview/c01271a0cad40962ed4936c012ff5632398c9a34?cid=9688e06282ff4043a95d46dee1f7467d
- https://p.scdn.co/mp3-preview/acf532e9831bc2dd5e5f3a6c0e92e1ed6d55beb7?cid=9688e06282ff4043a95d46dee1f7467d

album id: 
4HDJMKkwAMVFewqfZcmf84 (business as usual)
2ti2e8J05nwg9ikcMjW8aS (essential britney spears)

song id: 
3ZZq9396zv8pcn5GYVhxUi (down under)

artist id: 
0f3EsoviYnRKTkmayI3cux (men at work)


