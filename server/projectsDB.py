from pymongo import MongoClient

import hardwareDB

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
    projects = client.HardwareCheckout.Projects

    query = {'projectId': projectId}
    doc = projects.find_one(query)

    return doc


def createProject(client, projectName, projectId, description):
    projects = client.HardwareCheckout.Projects
    
    if projects.find_one({'projectId': projectId}) == None:
        doc = {
            'projectName': projectName,
            'projectId': projectId,
            'description': description,
            'hwSets': [],
            'users': []
        }
        projects.insert_one(doc)
        
        success = True
        message = 'Successfully added project'
    else:
        success = False
        message = 'Project ID already taken'

    return success, message


def addUser(client, projectId, userId):
    projects = client.HardwareCheckout.Projects

    filter = {'projectId': projectId}
    newValue = {'$push': {'users': userId}}
    projects.update_one(filter, newValue)


def updateUsage(client, projectId, hwSetName):
    projects = client.HardwareCheckout.Projects


def checkOutHW(client, projectId, hwSetName, qty, userId):
    projects = client.HardwareCheckout.Projects
    user = client.HardwareCheckout.People

    project = projects.find_one({'projectId': projectId})
    if project == None:
        return False, "Invalid project ID."
    elif userId not in project['users']:
        return False, "You are not a member of this project."
    elif hardwareDB.queryHardwareSet(client, hwSetName) == None:
        return False, "Hardware set does not exist."

    names = []
    for x in project['hwSets']:
        names.append(x.keys())
    
    if hwSetName not in names:
        projects.update_one({'projectId': projectId}, {'$push': {'hwSets': {hwSetName: int(qty)}}})
    else:
        usage = project['hwSets'][hwSetName]
        projects.update_one({'projectId': projectId}, {'$set': {'hwSets': {hwSetName: int(usage) + int(qty)}}})

    return hardwareDB.requestSpace(client, hwSetName, int(qty))


def checkInHW(client, projectId, hwSetName, qty, userId):
    projects = client.HardwareCheckout.Projects
    user = client.HardwareCheckout.People

    project = projects.find_one({'projectId': projectId})
    if project == None:
        return False, "Invalid project ID."
    elif userId not in project['users']:
        return False, "You are not a member of this project."
    elif hardwareDB.queryHardwareSet(client, hwSetName) == None:
        return False, "Hardware set does not exist."

    names = []
    for x in project['hwSets']:
        names.append(x.keys())
    
    if hwSetName not in names:
        projects.update_one({'projectId': projectId}, {'$push': {'hwSets': {hwSetName: -int(qty)}}})
    else:
        usage = project['hwSets'][hwSetName]
        projects.update_one({'projectId': projectId}, {'$set': {'hwSets': {hwSetName: int(usage) - int(qty)}}})

    return hardwareDB.requestSpace(client, hwSetName, -int(qty))
