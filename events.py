import os
from slack_sdk import WebClient

def getName(slackID):
    profile = client.users_info(
        user=slackID
    )
    name = profile.get("real_name")
    print(name)
