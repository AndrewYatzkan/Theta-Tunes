# to-do: add error handling

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv() # load environment variables (for authentication flow)

scope = "playlist-modify-private" # set scope for spotify api

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope)) # create spotipy object

# gets the URIs of tracks already on the playlist
def loadURIs(playlist):
	results = []
	tracks = sp.playlist_tracks(playlist)
	while tracks:
		trackURIs = list(map(lambda item : item["track"]["uri"], tracks["items"]))
		results.extend(trackURIs)
		if tracks["next"]:
			tracks = sp.next(tracks)
		else:
			tracks = None
	return results

# adds the list of URIs to the playlist
def addTracks(URIs, playlist="0Ub5rHeNVKSoSaJocpKBsa"):
	allTrackURIs = loadURIs(playlist) # fetch tracks so we don't add a duplicate
	print("Fetched track URIs")
	newTracks = list(filter(lambda uri : uri not in allTrackURIs, URIs))
	if newTracks:
		print("Adding %d new track(s)" % len(newTracks))
		sp.playlist_add_items(playlist, newTracks)
		print("Track(s) successfully added")
	else:
		print("No new tracks")

# to-do: load URIs that we want to be added
addTracks(["spotify:track:1lwvJQGhdq6Kyr4BBquf23", "spotify:track:0HsRWeoq9eME1Vgc8Evfhq"])