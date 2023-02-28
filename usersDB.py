from pymongo import MongoClient

def addUser(username, userid, password):
    client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")
    db = client.HardwareCheckout
    users = db.Users
    # Should check if username & userID are unique
    
    # Give list of projects they own?
    doc = {
        "Username": username,
        "UserID": userid,
        "Password": password
    }

    users.insert_one(doc)
    client.close()

# Might have to be private
# Can either query based on username or user ID
def queryUser(username):
    client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")
    db = client.HardwareCheckout
    users = db.Users

    query = {"Username": username}
    doc = users.find_one(query)
    client.close()

    return doc

