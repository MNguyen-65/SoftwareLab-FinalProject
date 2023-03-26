from pymongo import MongoClient

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

'''
Structure of Project entry so far:
Project = {
    'name': projectName,
    'projectid': projectID,
    'description': description
    'hwsets': {HW1: 0, HW2: 10, ...}
    'users': [user1, user2, ...]
}
'''

def addProject(projectName, projectID, description):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects
    
    if not projects.find({'name': projectName, 'projectid': projectID}):
        doc = {
            'name': projectName,
            'projectid': projectID,
            'description': description,
            'hwsets': {},
            'users': []
        }
        projects.insert_one(doc)
        
        success = True
        message = 'Successfully added project'
    else:
        success = False
        message = 'Project name or ID already taken'

    client.close()

    return success, message


def queryProject(projectID):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects

    query = {'projectid': projectID}
    doc = projects.find_one(query)
    client.close()

    return doc