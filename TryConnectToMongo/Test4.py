from pymongo import MongoClient

client = MongoClient("mongodb+srv://cluster0.jweue.mongodb.net")
db = client.test
col = db.tasklist
result = col.find( {"some field": "Michael"} )
for doc in result:
    # print the document's _id to terminal
    print ("doc _id:", doc["_id"])
