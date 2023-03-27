from pymongo import MongoClient

import projectsDB

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

'''
Structure of User entry so far:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

def addUser(username, userId, password):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    people = db.People

    existing_user = people.find_one({'username': username, 'userId': userId})
    if existing_user == None:
        doc = {
            'username': username,
            'userId': userId,
            'password': password,
            'projects': []
        }

        people.insert_one(doc)
        success = True
        message = 'Successfully added user'
    else:
        success = False
        message = 'Username or ID already taken'
        # u = existing_user['username']
        # uid = existing_user['userId']
        # pa = existing_user['password']
        # print(f'{u}, {uid}, {pa}')
    
    client.close()

    return success, message


def __queryUser(username, userId):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    people = db.People

    query = {'username': username, 'userId': userId}
    doc = people.find_one(query)
    client.close()

    return doc


def login(username, userId, password):
    doc = __queryUser(username, userId)

    # TODO: encrypt password here
    if(doc == None):
        return False, 'Invalid username or ID. Try again'
    elif(doc['password'] == password):
        return True, 'Login successful'
    else:
        return False, 'Invalid password. Try again'

def joinProject(userId, projectId):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    people = db.People

    success = False;
    userProjects = people.find_one({'userId': userId})['projects']

    if projectsDB.queryProject(projectId) == None:
        message = 'Project ID does not exist'
    elif projectId in userProjects:
        message = 'User is already in this project'
    else:
        filter = {'userId': userId}
        newValue = {'$push': {'projects': projectId}}
        people.update_one(filter, newValue)
        projectsDB.addUser(projectId, userId)
        success = True;
        message = 'Successfully added project'

    client.close()

    return success, message
