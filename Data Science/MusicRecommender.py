import os
from dotenv import load_dotenv
import sys
import json
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

scope = 'user-top-read'
oauth_obj = sp.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
token = oauth_obj.get_access_token(as_dict=False)
spotifyObj = sp.Spotify(auth=token)
username = spotifyObj.current_user()

top_tracks = spotifyObj.current_user_top_tracks(limit = 5)['items']
# pd.DataFrame.to_csv(top_tracks, 'top_tracks.csv')
tracks = pd.DataFrame()
names = []
for track in top_tracks:
    uri = track['uri']
    name = track['name']
    result = spotifyObj.audio_features(uri)
    tracks.add(result)
    names.append(name)
    
i = 0
print(type(tracks))


vectors = []
i = 0
for track in tracks:
    tracks[i][1].drop(['key', 'mode', 'type', 'id', 'uri'])
    i += 1 
    
print(tracks)
# pd.DataFrame.to_csv(tracks, 'cleaned.csv')

# audio_features = spotifyObj.audio_features(liked_songs['href'])

# Read in dataset of songs
tracks = pd.read_csv('Data Science\SpotifyFeatures.csv')

# Data cleaning
popular_tracks = tracks.drop(['duration_ms', 'key', 'mode', 'time_signature'], axis=1).sort_values('popularity', ascending=True)
popular_tracks = popular_tracks.loc[popular_tracks['popularity'] >= 50]


