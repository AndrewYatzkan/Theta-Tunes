from groupy import Client
import requests
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
group_to_send = None
for group in client.groups.list():
    if (group.name == "Spotify bot"):
        messages = group.messages.list_all()
        group_to_send = group

for message in messages:
    if "open.spotify.com/track" in message.text:
        spotify_id = message.text[31:53]
        request_url = 'https://api.spotify.com/v1/tracks/' + spotify_id
        test = requests.get(request_url, headers=headers)
        test = test.json()
        text_to_send = "song URI found: "+ test['uri']
        group_to_send.post(text=text_to_send)