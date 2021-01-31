from slack import WebClient
from managerbot import ManagerBot
import os
import time
#from datetime import datetime, timedelta
#from threading import Timer

# Create a slack client
slack_web_client = WebClient(token=os.environ.get("BOT_USER_TOKEN"))
while True:

# Get a new CoinBot
    manager_bot = ManagerBot("#general")

# Get the onboarding message payload
    message = manager_bot.get_automated_early_message_payload()

# Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)

    time.sleep(28800)

    manager_bot2 = ManagerBot("#general")

    # Get the onboarding message payload
    message2 = manager_bot2.get_automated_late_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message2)
    time.sleep(57600)
