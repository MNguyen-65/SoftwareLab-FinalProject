from pymongo import MongoClient

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

'''
Structure of Project entry so far:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description
    'hwSets': {HW1: 0, HW2: 10, ...}
    'users': [user1, user2, ...]
}
'''

def queryProject(projectId):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects

    query = {'projectId': projectId}
    doc = projects.find_one(query)
    client.close()

    return doc


def createProject(projectName, projectId, description):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects
    
    if projects.find_one({'projectId': projectId}) == None:
        doc = {
            'projectName': projectName,
            'projectId': projectId,
            'description': description,
            'hwSets': {},
            'users': []
        }
        projects.insert_one(doc)
        
        success = True
        message = 'Successfully added project'
    else:
        success = False
        message = 'Project ID already taken'

    client.close()

    return success, message


def addUser(projectId, userid):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects

    filter = {'projectId': userid}
    newValue = {'$push': {'users': projectId}}
    projects.update_one(filter, newValue)
    
    client.close()