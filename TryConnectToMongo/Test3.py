import pymongo



client = pymongo.MongoClient("mongodb+srv://cluster0.jweue.mongodb.net")
db = client[ "testdb" ] # makes a test database called "testdb"
col = db[ "testcol" ] #makes a collection called "testcol" in the "testdb"
#add a document to testdb.testcol

print(client.server_info)
