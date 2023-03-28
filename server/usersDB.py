from pymongo import MongoClient

import projectsDB

'''
Structure of User entry so far:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

def addUser(client, username, userId, password):
    people = client.HardwareCheckout.People

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
    
    return success, message


def __queryUser(client, username, userId):
    people = client.HardwareCheckout.People

    query = {'username': username, 'userId': userId}
    doc = people.find_one(query)

    return doc


def login(client, username, userId, password):
    user = __queryUser(client, username, userId)

    # TODO: encrypt password here
    if(user == None):
        return False, 'Invalid username or ID. Try again'
    elif(user['password'] != password):
        return False, 'Invalid password. Try again'
    return True, 'Login successful'


def joinProject(client, userId, projectId):
    people = client.HardwareCheckout.People

    success = False;
    userProjects = people.find_one({'userId': userId})['projects']

    if projectsDB.queryProject(client, projectId) == None:
        message = 'Project ID does not exist'
    elif projectId in userProjects:
        message = 'User is already in this project'
    else:
        filter = {'userId': userId}
        newValue = {'$push': {'projects': projectId}}
        people.update_one(filter, newValue)
        projectsDB.addUser(client, projectId, userId)
        success = True;
        message = 'Successfully added project'

    return success, message


def getUserProjects(client, userId):
    people = client.HardwareCheckout.People

    userProjects = people.find_one({'userId': userId})['projects']
    projects = []

    for projectId in userProjects:
        projects.append(projectsDB.queryProject(client, projectId))

    return projects
