from groupy import Client
import re

client = Client.from_token(token)
messages = None
group_to_send = None
for group in client.groups.list():
    if (group.name == "Spotify bot"):
        messages = group.messages.list_all()
        group_to_send = group

for message in messages:
    x = re.findall("https:\/\/open\.spotify\.com\/track\/([0-9A-z]{22})", message.text)
    for uri in x:
        group_to_send.post(uri)