
import pymongo

client = pymongo.MongoClient("mongodb+srv://amv:mchacks8@cluster0.jweue.mongodb.net/test?retryWrites=true&w=majority")
db = client.Employee_Data
collection = db['task_info']
dataList = collection.find()

def getEmployeesByProject(project):
    employees = ""
    for item in dataList:
        if (item["Project"].lower() in project.lower()):
            employees = employees + item["Name"] + ", "
    employees = employees[:-2]
    return employees

def getStatusReport(name):
    report = "No report available"
    for item in dataList:
        if (item["Name"].lower() in name.lower()):
            report = "" + item["Status"]
    return report

def getAllTasks(name):
    tasklist = ""
    for item in dataList:
        if (item["Name"].lower() in name.lower()):
            for task in item["Tasks"]:
                tasklist = tasklist + task + ", "
            tasklist = tasklist[:-2]
    return tasklist

def getCompletedTasks(name):
    completed = ""
    for item in dataList:
        if (item["Name"].lower() in name.lower()):
            for complete in item["Completed_Tasks"]:
                completed = completed + complete + ", "
            completed = completed[:-2]
    return completed

def getStatusReport(name):
    report = "No report available"
    for item in datalist:
        if (item["Name"].lower() in name.lower()):
            report = "" + item["Status"]
    return report

def getEmployeeList():
    names = []
    for item in dataList:
        names.append(item["Name"])
    return names

def getEmployeeProject(name):
    project = "No project assigned"
    name = name.lower()
    for item in dataList:
        if (item["Name"].lower() in name.lower()):
            project = "" + item["Project"]
    return project

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
