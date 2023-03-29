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


def addUser(client, projectId, userId):
    projects = client.HardwareCheckout.Projects

    filter = {'projectId': projectId}
    newValue = {'$push': {'users': userId}}
    projects.update_one(filter, newValue)


def updateUsage(client, projectId, hwSetName):
    projects = client.HardwareCheckout.Projects



def checkOutHW(client, projectId, hwSetName):
    projects = client.HardwareCheckout.Projects

    projects.update_one(
        {'projectId': projectId}, 
        {'$push': 
            {'hwSets': 
                {hwSetName: 0}
            }
        }
    )


def checkOutHW(client, projectId, hwSetName):
    projects = client.HardwareCheckout.Projects

    used = projects.find_one({'projectId': projectId})['hwSets'][hwSetName]

    hardwareDB.requestSpace(client, hwSetName, -used)
    projects.update_one(
        {'projectId': projectId}, 
        {'$pull': 
            {'hwSets': 
                {hwSetName: used}
            }
        }
    )
