from flask import Flask, render_template, request, redirect, session
import os
import openai
import asyncio
import spotipy
from config import sid, sid_sec
import time

chatgpt = os.environ['CHATTOKEN']
app = Flask(__name__, static_folder="static")
app.secret_key = "secret"
openai.api_key = chatgpt
CLI_ID = sid
CLI_SEC = sid_sec
# Make sure you add this to Redirect URIs in the setting of the application dashboard
REDIRECT_URI2 = "https://f68ef816-f7ea-4c45-b66a-0e9a8cf69a0e-00-hmrkn8piyx5b.worf.replit.dev:3000/api_callback"
REDIRECT_URI = "https://testing-render-8isd.onrender.com/api_callback"

SCOPE = 'user-read-recently-played, user-top-read'

# Set this to True for testing but you probaly want it set to False in production.
SHOW_DIALOG = True
API_BASE = 'https://accounts.spotify.com'


def resp(prompt):
  engine = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {
              "role": "user",
              "content": prompt,
          },
      ],
  )
  print(engine)
  return engine.choices[0].message.content


def get_token(session):
  token_valid = False
  token_info = session.get("token_info", {})

  # Checking if the session already has a token stored
  if not (session.get('token_info', False)):
    token_valid = False
    return token_info, token_valid

  # Checking if token has expired
  now = int(time.time())
  is_token_expired = session.get('token_info').get('expires_at') - now < 60

  # Refreshing token if it has expired
  if (is_token_expired):
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID,
                                           client_secret=CLI_SEC,
                                           redirect_uri=REDIRECT_URI,
                                           scope=SCOPE)
    token_info = sp_oauth.refresh_access_token(
        session.get('token_info').get('refresh_token'))

  token_valid = True
  return token_info, token_valid


@app.route("/verify")
def verify():
  # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
  sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID,
                                         client_secret=CLI_SEC,
                                         redirect_uri=REDIRECT_URI,
                                         scope=SCOPE)
  auth_url = sp_oauth.get_authorize_url()
  print(auth_url)
  return redirect(auth_url)


@app.route("/api_callback")
def api_callback():
  # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
  sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLI_ID,
                                         client_secret=CLI_SEC,
                                         redirect_uri=REDIRECT_URI,
                                         scope=SCOPE)
  session.clear()
  code = request.args.get('code')
  token_info = sp_oauth.get_access_token(code)

  # Saving the access token along with all other token related info
  session["token_info"] = token_info

  return redirect("/")


@app.route('/')
def home():
  if session:
    songs = most()
    print(type(songs))
    return render_template("home.html", songs=songs)
  else:
    return render_template("index.html")


@app.route("/logout")
def logout():
  if session:
    session.clear()
    return redirect("/")
  else:
    return redirect("/")


@app.route('/getsongs', methods=["POST", "GET"])
def getsongs():
  if request.method == "POST":
    print(request.json)
    prompt = f"from this list of ranked songs, recommend 9 other songs and 1 opposing style song: {request.json}. also recommend 1 movie, 1 game and 1 book that would have similar vibe to the songs"
    data = resp(prompt)
    print(data)
    data = str(data)
    data = data.replace("\n", ", <br>").replace("\\", "")

    return {"data": data}  # You can return a string as an example response
  else:
    return redirect('/')


def most():
  session['token_info'], authorized = get_token(session)
  session.modified = True
  if not authorized:
    return redirect('/')
  sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
  resulter = sp.current_user_top_tracks(limit=10, time_range="short_term")
  played = []
  tracks = {}
  for idx, item in enumerate(resulter['items']):
    track = item['name']
    print(item)
    image = item['album']['images'][0].get('url')
    print(image)
    artist = item['artists'][0]['name']
    print(artist)
    #song = track['name']
    #print(song)
    tracks[image] = artist + " - " + track

  return tracks


@app.route('/foundsongs')
def index():
  #data = resp()

  return render_template("songs.html", data=data)


app.run(host='0.0.0.0', port=80)
