from pymongo import MongoClient

MONGODB_SERVER = "mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority"

'''
Structure of User entry so far:
User = {
    "Username": username,
    "UserID": userid,
    "Password": password,
    "Projects": [project1_ID, project2_ID, ...]
}
'''

def addUser(username, userid, password):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    users = db.Users
    success = False

    # Should check if username & userID are unique
    if users.find({"Username": username, "UserID": userid}).count() == 0:
        # Give list of projects they own?
        doc = {
            "Username": username,
            "UserID": userid,
            "Password": password
        }

        users.insert_one(doc)
        success = True
    
    client.close()

    return success

# Don't want user accessing documents directly
def __queryUser(username, userid):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    users = db.Users

    query = {"Username": username, "UserID": userid}
    doc = users.find_one(query)
    client.close()

    return doc

# Idea: return -1 for user doesn't exist, 0 for incorrect
#       password, and 1 for successful login
def login(username, userid, password):
    doc = __queryUser(username, userid)
    if(doc == None):
        # User doesn't exist
        return False
    # TODO: encrypt password here
    return doc['password'] == password

# def addProject(username, userid, projectID):
