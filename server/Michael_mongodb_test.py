from pymongo import MongoClient

# client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/test")
client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")
db = client.HardwareCheckout
posts = db.HardwareSets
print(posts.find())
db = client.HardwareCheckout

post = {
    "Description": "Hardware Set a milli",
    "Capacity": "200",
    "Availability": "200"
}

post_id = posts.insert_one(post).inserted_id
print(post)
