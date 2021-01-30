# Python code to illustrate
# inserting data in MongoDB
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://cluster0.jweue.mongodb.net")


client.server_info()
db = client.test
collection = db.tasklist

for data in collection:
    print(data)
