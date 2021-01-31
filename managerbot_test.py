from slack import WebClient
from managerbot import ManagerBot
import os
import xlrd
import time
from datetime import datetime, timedelta

# Create a timestamp for tomorrow at 9AM
#today = datetime.date.today()
#scheduled_time = datetime.time(hour=19, minute=50)
#schedule_timestamp = datetime.datetime.combine(today, scheduled_time).strftime('%s')



slack_web_client = WebClient(token=os.environ.get("BOT_USER_TOKEN"))

while True:
#def funcSend():
    # Create a slack client


    # Get a new CoinBot
    manager_bot = ManagerBot("#general")

    # Get the onboarding message payload
    message = manager_bot.get_automated_early_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)
    time.sleep(86400)
