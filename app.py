from flask import Flask, Response
from slackeventsapi import SlackEventAdapter
import os
from threading import Thread
from slack import WebClient
import json
import pymongo

client = pymongo.MongoClient("mongodb+srv://amv:mchacks8@cluster0.jweue.mongodb.net/test?retryWrites=true&w=majority")
db = client.Employee_Data
collection = db['task_info']
dataList = collection.find()

def updatingProjectData(namegiven, projects):
    for item in dataList:
        if(item["Name"] == namegiven):
            myquery = { "Name": namegiven}
            newvalues = { "$set": { "Project": projects}}
            collection.update_one(myquery, newvalues)

def moveTaskToCompleted(namegiven,task):
    for item in dataList:
        for data in item["Tasks"]:
            if(item["Name"] == namegiven and data == task):
                #myquerys = { "Tasks": data}
                collection.update_one(
                  { "Name": namegiven },
                  { "$pull": { "Tasks": task } }
                )
                collection.update_one(
                    { "Name": namegiven},
                    {"$push": {"Completed_Tasks": task} }
                )
def addTask(namegiven, task):
    for item in dataList:
        if(item["Name"] == namegiven):
            collection.update_one(
                { "Name": namegiven},
                {"$push": {"Tasks": task}}
                )
#dataList.sort({"Productivity":-1}).limit(1) // for MAX

def employeeRec(projects):
    for item in dataList:
        if(item["Project"] == projects and item["Productivity"] > str(8.5)):
            print("I recommend you assign the task to this employee: " + item["Name"])

            #collection.update_one(
            #{ "Project": projects},
            #{"$push": {"Tasks": task}}
            #)

# This `app` represents your existing Flask app
app = Flask(__name__)

# priority order: reminders > timers > helpers > finishers > productivity > thankings > greetings

#keep updated list of names of people in the slack workspace using the database
vague=["add", "assign", "give", "a job", "put"]
tasks = ["task"]
projects = ["another team", "project"]
names=["Violet", "Alex", "Michael"]
#if a new user joins the slack, make a trigger that adds them to the list of names and gives them a database entry
deadlines=["make sure", "is completed by", "change the deadline", "done by", "on my desk"]
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

def get_user_name(message):
    userid = message["user"]
    userdata=slack_client.users_info(user = userid)
    name = userdata["user"]["real_name"]
    return name

actionName = None
task = None
project = None

@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        global actionName
        global task 
        global project
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
                #different dialgue for owner
                if (userIsOwner == True):
                    for name in names:
                        if (name.lower() in command.lower()):
                            actionName = name
                            if ("task" in command.lower()):
                                response = (
                                "Hello, what task would you like to assign " +actionName+ "? Please include 'Task:' before your request."
                                    #% message["user"]   # noqa
                                )
                                known = True
                                break
                            elif ("status report" in command.lower()):
                                #send status report from database
                                response = (
                                "Here is the status report. Can I help with anything else?"
                                    #% message["user"]
                                )
                                known = True
                                break
                            else: 
                                for proj in projects:
                                    if(proj in command.lower()):
                                        response = (
                                        "Hello, what project would you like to assign " +actionName+ "? Please include 'project:' before your request."
                                             #% message["user"]   # noqa
                                        )
                                        known = True
                                        break
                                    else:
                                        response = (
                                        "Would you like to assign " +actionName+ " another task? A new project? Or get a status report?"
                                            #% message["user"]
                                        )
                                        known = True
                                        break

                    if (actionName is None):
                        response = (
                        "Please specify a user along with this action."
                            #% message["user"]
                        )
                        known = True
                        break
                    for item in vague:
                        if(item in command.lower()):
                            response = (
                            "Please be more specific with your request. Task? Project? Or status report?"
                                #% message["user"]
                            )
                            known = True
                            break

                    if("task:" in command.lower()):
                        task = command
                        addTask(actionName, task[19:])
                        #send task to database
                        response = (
                        "The task has been assigned to " + actionName +". Can I help with anything else?"
                            #% message["user"]
                        )
                        known = True
                    elif("task" in command.lower() and  not (actionName is None)):

                        #send task to database
                        response = (
                        "Hello, what task would you like to assign " +actionName+ "? Please include 'Task:' before your request."
                            #% message["user"]
                        )
                        known = True 
                    if ("project:" in command.lower()):
                        project = command
                        updatingProjectData(str(actionName), str(project[24:]))
                        #send project to database
                        response = (
                        actionName +" has been assigned to the project. Can I help with anything else?"
                            #% message["user"]
                        )
                        actionName = None
                        known = True
                    elif ("project" in command.lower() and not (actionName is None)):
                        #send project to database
                        response = (
                        "Hello, what project would you like to assign " +actionName+ "? Please include 'project:' before your request."
                            #% message["user"]
                        )
                        known = True
                        
                #if not an owner, treat as employee
                else:
                    for greeting in greetings:
                        if (greeting in command.lower()):
                            response = (
                            "Hello <@%s>! :tada:"
                                % message["user"]  # noqa
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
                    #TODO: Send message with formatting 
                    for finisher in finishers:
                        if (finisher in command.lower()):
                            #moveTaskToCompleted(get_user_name(message), task[19:])
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
                known = True
            slack_client.chat_postMessage(channel=channel_id, text=response)
    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=3000)
