from pymongo import MongoClient

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

def queryProject(client, projectId):
    db = client.HardwareCheckout
    projects = db.Projects

    query = {'projectId': projectId}
    doc = projects.find_one(query)

    return doc


def createProject(client, projectName, projectId, description):
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

    return success, message


def addUser(client, projectId, userid):
    db = client.HardwareCheckout
    projects = db.Projects

    filter = {'projectId': userid}
    newValue = {'$push': {'users': projectId}}
    projects.update_one(filter, newValue)