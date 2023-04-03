from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

import usersDB
import projectsDB
import hardwareDB

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

app = Flask(__name__)

# WORKING
# Function tries to login a user with their provided username and Password
# Returns json specfiying if the user login attempt was successful or not
@app.route('/login', methods=['POST'])
def login():
    # user_id = request.args.get('userId', None)
    # print(f"User Portal for user ID: {user_id}")
    username = request.json.get('username') # username, password are taken in from the webpage html
    userId = request.json.get('userId')
    password = request.json.get('password')

    client = MongoClient(MONGODB_SERVER)
    success, message = usersDB.login(client, username, userId, password)
    client.close()

    return jsonify({'success': success, 'message': message, 'userId': userId})

# work in progress
@app.route('/main')
def mainPage():
    user_id = request.args.get('userId', None)
    print(f"/main User Portal for user ID: {user_id}")
    # username = request.json.get('username') # username, password are taken in from the webpage html
    # userId = request.json.get('userId')
    # password = request.json.get('password')

    client = MongoClient(MONGODB_SERVER)
    projects = usersDB.getUserProjects(client)
    client.close()

    return jsonify({'success': success, 'userId': userId})

@app.route('/join_project', methods=['POST'])
def join_project():
    projectId = request.json.get('projectId')
    userId = request.json.get('userId')

    client = MongoClient(MONGODB_SERVER)
    success, message = usersDB.joinProject(client, userId, projectId)
    client.close()

    return jsonify({'success': success, 'message': message})



# NOT SURE IF WORKING
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


@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    userId = request.json.get('userId')

    client = MongoClient(MONGODB_SERVER)
    projects = usersDB.getUserProjectsList(client, userId)
    client.close()

    return jsonify({'projects': projects})


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


@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    projectId = request.json.get('projectId')

    client = MongoClient(MONGODB_SERVER)
    project = projectsDB.queryProject(client, projectId)
    projectName = project['projectName']
    description = project['description']
    hwSets = str(project['hwSets'])
    users = project['users']
    client.close()

    return jsonify({'projectName': projectName, 
                    'description': description, 
                    'hwSets': hwSets, 
                    'users': users})


@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    client = MongoClient(MONGODB_SERVER)
    hwNames = hardwareDB.getAllHwNames(client)
    client.close()

    return jsonify({'hwNames': hwNames})


@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    hwName = request.json.get('hwName')

    client = MongoClient(MONGODB_SERVER)
    hwSet = hardwareDB.queryHardwareSet(client, hwName)
    avail = hwSet['availability']
    cap = hwSet['capacity']
    client.close()

    return jsonify({'availability': avail, 'capacity': cap})


@app.route('/check_out', methods=['POST'])
def check_out():
    projectId = request.json.get('projectId')
    hwSetName = request.json.get('hwSetName')
    qty = request.json.get('qty')
    userId = request.json.get('userId')

    client = MongoClient(MONGODB_SERVER)
    success, message = projectsDB.checkOutHW(client, projectId, hwSetName, qty, userId)
    if hardwareDB.queryHardwareSet(client, hwSetName) == None:
        avail = 0
        cap = 0
    else:
        hwset = hardwareDB.queryHardwareSet(client, hwSetName)
        avail = hwset['availability']
        cap = hwset['capacity']
    client.close()

    return jsonify({'success': success, 'message': message, 'avail': avail, 'cap': cap})


@app.route('/check_in', methods=['POST'])
def check_in():
    projectId = request.json.get('projectId')
    hwSetName = request.json.get('hwSetName')
    qty = request.json.get('qty')
    userId = request.json.get('userId')

    client = MongoClient(MONGODB_SERVER)
    success, message = projectsDB.checkInHW(client, projectId, hwSetName, qty, userId)
    if hardwareDB.queryHardwareSet(client, hwSetName) == None:
        avail = 0
        cap = 0
    else:
        hwset = hardwareDB.queryHardwareSet(client, hwSetName)
        avail = hwset['availability']
        cap = hwset['capacity']
    client.close()

    return jsonify({'success': success, 'message': message, 'avail': avail, 'cap': cap})


@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    hwSetName = request.json.get('name')
    initCapacity = request.json.get('initCapacity')

    client = MongoClient(MONGODB_SERVER)
    success, message = hardwareDB.createHardwareSet(client, hwSetName, initCapacity)
    client.close()

    return jsonify({'success': success, 'message': message})


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