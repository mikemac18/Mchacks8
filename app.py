from flask import Flask, Response
from slackeventsapi import SlackEventAdapter
import os
from threading import Thread
from slack import WebClient
import json


# This `app` represents your existing Flask app
app = Flask(__name__)

# priority order: reminders > timers > helpers > finishers > productivity > thankings > greetings
greetings = ["hi", "hello", "hello there", "hey", "greetings", "good morning" ]
reminders = ["set a reminder","send me a reminder", "remind me", "set a timer", "set timer", "set reminder", "make a reminder", "send a reminder", "create a reminder", "create reminder", "reminders", "reminder"]
helpers = ["help", "i am lost", "confused", "stuck", "i'm lost", "team members", "task members", "task members", "working with" ]
finishers = ["finished", "done", "completed", "complete"]
productivities = ["productivity", "how am i doing", "is my timing", "score"]
thankings = ["thank you", "thanks"]
timers = [":", "am", "pm", "oclock", "o'clock"]

SLACK_SIGNING_SECRET = os.environ['SLACK_EVENTS_TOKEN']
slack_token = os.environ['BOT_USER_TOKEN']
VERIFICATION_TOKEN = os.environ['VERIFICATION_TOKEN']

#instantiating slack client
slack_client = WebClient(slack_token)

# An example of one of your Flask app's routes
@app.route("/")
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)

def get_user_permission(message):
    userid = message["user"]
    userdata=slack_client.users_info(user = userid)
    permissioncheck = userdata["user"]["is_owner"]
    return permissioncheck

@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            known = False
            channel_id = message["channel"]
            userIsOwner = get_user_permission(message)
            score = 4
            response = (
            "I'm not sure what you are saying. Could you try rephrasing?"
            )
            while (known == False):
                for greeting in greetings:
                    if (greeting in command.lower()):
                        response = (
                        "Hello <@%s>! :tada:"
                            % message["user"]  # noqa
                        )
                        if (userIsOwner == True):
                            response = (
                            "Hey <@%s>, do you want to set tasks?"
                                 % message["user"]   # noqa
                            )
                        known = True
                for reminder in reminders:
                    if (reminder in command.lower()):
                        response = (
                        "Make sure you include a time for when you want your reminder."
                        )
                        for timer in timers:
                            if (timer in command.lower()):
                                response = (
                                "Reminder set for <@%s>"
                                    % message["user"]
                                )
                                known = True

                        known = True

                for helper in helpers:
                    if (helper in command.lower()):
                        response = (
                        "Other task members include: <@%s> . Don't be afraid to ask for help!"
                            % message["user"]
                        )
                        known = True
                for finisher in finishers:
                    if (finisher in command.lower()):
                        response = (
                        "Keep up the good work! Your completion time has been logged for task <@%s>. Onto the next one!"
                            % message["user"]
                        )
                        known = True
                for productivity in productivities:
                    if (productivity in command.lower()):
                        if (score < 3):
                            response = (
                            "Looks like you need to pick up the pace. You can do it!"
                        )
                        elif (score >= 3 or score <=7):
                            response = (
                            "I like your steady pace! Keep it up."
                        )
                        elif (score < 7):
                            response = (
                            "You are doing great! Thanks for your hard work."
                        )
                        known = True
                for thanking in thankings:
                    if (thanking in command.lower()):
                        response = (
                        "You're welcome!"
                        )
                        known = True
                known = True
            slack_client.chat_postMessage(channel=channel_id, text=response)
    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=3000)
