from groupy import Client
import requests
import spotify
import json



AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': spot_id,
    'client_secret': spot_secret,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

client = Client.from_token(token)
messages = None

uris = []
for group in client.groups.list():
    if group.name == "Spotify bot":
        messages = group.messages.list_all()

for message in messages:
    if "open.spotify.com/track" in message.text:
        message.like()

        link_idx = message.find("open.spotify.com")
        spotify_id = message.text[link_idx + 31: link_idx + 53]

        request_url = 'https://api.spotify.com/v1/tracks/' + spotify_id

        test = requests.get(request_url, headers=headers)
        test = test.json()

        uris.append(test['uri'])

spotify.addTracks(uris)