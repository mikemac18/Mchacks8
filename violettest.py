import pymongo
import dns


client = pymongo.MongoClient("mongodb+srv://amv:mchacks8@cluster0.jweue.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

collist = db.list_collection_names()

print(collist)
