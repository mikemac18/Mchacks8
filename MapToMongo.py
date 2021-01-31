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
employeeRec("A")

#addTask("Michael","4")
#moveTaskToCompleted("Michael","4")
#updatingProjectData("Michael", "Newer")

# Insert Data
#rec_id1 = collection.insert_one(emp_rec1)
#rec_id2 = collection.insert_one(emp_rec2)