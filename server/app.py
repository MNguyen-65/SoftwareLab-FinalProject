from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

import usersDB
import projectsDB
import hardwareDB

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

app = Flask(__name__)


# Function tries to login a user with their provided username and Password
# Returns json specfiying if the user login attempt was successful or not
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username') # username, password are taken in from the webpage html
    userId = request.json.get('userId')
    password = request.json.get('password')

    client = MongoClient(MONGODB_SERVER)
    success, message = usersDB.login(client, username, userId, password)
    client.close()

    return jsonify({'success': success, 'message': message})


# Function tries to create a user with their provided username and Password
# Returns json specfiying if the user creation was successful or not
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.json.get('username')
    userId = request.json.get('userId')
    password = request.json.get('password')

    client = MongoClient(MONGODB_SERVER)
    success, message = usersDB.addUser(client, username, userId, password)
    client.close()

    return jsonify({'success': success, 'message': message})


@app.route('/get_user_projects', methods=['GET'])
def get_user_projects():
    userId = request.json.get('userId')

    client = MongoClient(MONGODB_SERVER)
    projects = usersDB.getUserProjects(client)
    client.close()

    return jsonify(projects)


@app.route('/create_project', methods=['POST'])
def create_project():
    userId = request.json.get('userId')
    projectName = request.json.get('projectName')
    projectId = request.json.get('projectId')
    description = request.json.get('description')

    client = MongoClient(MONGODB_SERVER)
    success, message = projectsDB.createProject(client, projectName, projectId, description)
    if not success:
        client.close()
        return jsonify({'success': success, 'message': message})
    
    success, message = usersDB.joinProject(client, userId, projectId)
    client.close()

    return jsonify({'success': success, 'message': message})


@app.route('/join_project', methods=['POST'])
def join_project():
    userId = request.json.get('userId')
    projectId = request.json.get('projectId')
    
    client = MongoClient(MONGODB_SERVER)
    success, message = usersDB.joinProject(client, userId, projectId)
    client.close()

    return jsonify({'success': success, 'message': message})


@app.route('/add_hardware', methods=['POST'])
def add_hardware_set():
    hwSetName = request.json.get('name')
    initCapacity = request.json.get('initCapacity')

    client = MongoClient(MONGODB_SERVER)

    db = client.HardwareCheckout
    hwsets = db.HardwareSets
    
    doc = {
        'name': hwSetName,
        'capacity': str(initCapacity),
        'availability': str(initCapacity)
    }

    hwsets.insert_one(doc)

@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    print('testing check inv')
    client = MongoClient(MONGODB_SERVER)

    projects = []
    for project in client.HardwareCheckout.Projects.find():
        projects.append({
            'name': project['name'],
            'projectId': project['projectId'],
            'description': project['description']
            
            # add more fields as needed
        })
    return jsonify(projects)


if __name__ == '__main__':
    app.run()