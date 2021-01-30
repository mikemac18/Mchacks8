from pymongo import MongoClient
uri = "mongodb+srv://cluster0.jweue.mongodb.net/<dbname>?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='<path_to_certificate>')
db = client['testDB']
collection = db['testCol']
doc_count = collection.count_documents({})
print(doc_count)
