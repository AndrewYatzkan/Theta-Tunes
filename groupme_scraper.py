from groupy import Client
import dotenv
import os
import re

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

MOST_RECENT_MESSAGE_ID = os.environ["MOST_RECENT_MESSAGE_ID"]

GROUPME_ACCESS_TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]

client = Client.from_token(GROUPME_ACCESS_TOKEN)

def getBot(botName, groupId):
    for bot in client.bots.list():
        if bot.group_id == groupId and bot.name == botName:
            return bot

# to-do: list_all() is unnecessary, use list() until we've seen the page before
def getMessages(groupId):
    for group in client.groups.list():
        if group.id == groupId:
            return group.messages.list_all()

def getURIs(messages):
    firstMessage = True
    URIs = []
    for message in messages:
        # Changes most recent message in .env file - Assumes the following code won't error
        if firstMessage:
            firstMessage = False
            dotenv.set_key(dotenv_file, "MOST_RECENT_MESSAGE_ID", message.id)
        # Returns if we've seen this message before
        if message.id == MOST_RECENT_MESSAGE_ID:
            return URIs
        if message.text is not None:
            # Matches spotify URL pattern
            x = re.findall("https:\/\/open\.spotify\.com\/track\/([0-9A-z]{22})", message.text)
            for trackId in x:
                URIs.append("spotify:track:" + trackId)
    # If it's the first time running in this group:
    return URIs