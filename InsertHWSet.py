from pymongo import MongoClient

client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/test")
db = client.HardwareCheckout
posts = db.HardwareSets

post = {
    "Description": "Hardware Set 3",
    "Capacity": "200",
    "Availability": "200"
}

post_id = posts.insert_one(post).inserted_id
print(post)