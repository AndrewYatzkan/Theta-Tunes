# to-do: add error handling
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import logging

# silences errors when trackExists returns false
logger = logging.getLogger("spotipy")
logger.setLevel(logging.CRITICAL)

load_dotenv() # load environment variables (for authentication flow)

scope = "playlist-modify-private" # set scope for spotify api

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope)) # create spotipy object

# to-do: temporarily silence stdout when sp.track is called
def trackExists(uri):
	try:
		sp.track(uri)
		return True
	except spotipy.exceptions.SpotifyException:
		return False

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
def addTracks(URIs, playlist):
	allTrackURIs = loadURIs(playlist) # fetch tracks so we don't add a duplicate
	print("Fetched track URIs")
	newTracks = list(filter(lambda uri : uri not in allTrackURIs and trackExists(uri), list(set(URIs))))
	# for uri in newTracks:
		# sp.track(uri)
	if newTracks:
		print("Adding %d new track(s)" % len(newTracks))
		sp.playlist_add_items(playlist, newTracks)
		print("Track(s) successfully added")
		return len(newTracks)
	else:
		print("No new tracks")