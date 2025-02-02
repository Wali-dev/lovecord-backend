from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config
from model import post
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins = Config.CORS_ALLOWED_ORIGINS)

try:
    song_model = post()
except Exception as e:
    print(f"Failed to initialze SongMode: {e}")
    exit(1)
    
#Spotify api setup
sp_oauth = SpotifyOAuth(
    client_id = Config.SPOTIPY_CLIENT_ID,
    client_secret = Config.SPOTIPY_CLIENT_SECRET,
    redirect_uri = Config.SPOTIPY_REDIRECT_URI,
    scope = Config.SPOTIPY_SCOPE,
)



@app.route('/', methods=["GET"])
def index():
    if "token_info" in session:
        sp = spotipy.Spotify(auth_manager = sp_oauth)
        try:
            top_tracks = sp.current_user_top_tracks(limit=10)
            seed_tracks = [track['id'] for track in top_tracks['items']]
            recommendations = sp.recommendations(seed_tracks=seed_tracks, limit = 10)
            
            return render_template("index.html", user_profile=sp.me(), top_tracks = top_tracks['items'], recommendations = recommendations['tracks'])
        except spotipy.SpotipyException as e:
            print(f"Spotify API Error: {e}")
            return render_template("index.html", user_profile=sp.me())
        
    return render_template("index.html")


@app.route("/send_song", methods=["POST"])
def send_song():
    try:
        recipent_name = request.form.get("recipent_name")
        message = request.form.get("message")
        
        sp = spotipy.Spotify(aouth_manager=sp_oauth)
        track_id = request.form.get("track_id")
        track = sp.track(track.id)
        song_name = track['name']
        
        song_data = {
             "recipient_name": recipient_name,
             "message": message,
             "song_name": song_name,
        }





if __name__ == '__main__':
    app.run(debug=True)