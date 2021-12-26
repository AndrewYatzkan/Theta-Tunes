from dotenv import load_dotenv
import groupme_scraper as groupme
import spotify
import os

botName = os.getenv("GROUPME_BOT_NAME")
groupId = os.getenv("GROUPME_GROUP_ID")
playlistId = os.getenv("SPOTIFY_PLAYLIST_ID")

chatBot = groupme.getBot(botName, groupId)
messages = groupme.getMessages(groupId)

URIs = groupme.getURIs(messages)

newTracks = spotify.addTracks(URIs, playlistId)

if newTracks:
	print(str(newTracks) + " track(s) added to the playlist!")
	chatBot.post(str(newTracks) + " track(s) added to the playlist!")
else:
	print("No tracks added to the playlist.")