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

@app.route('/join_project', methods=['GET'])
def join_project():
    project_id = request.args.get('projectId', None)
    user_id = request.args.get('userId', None)
    print(f"debug join project: {project_id} {user_id}")


    client = MongoClient(MONGODB_SERVER)
    db = client['HardwareCheckout']
    project = db.Projects.find_one({"projectId": project_id})
    # project = client.HardwareCheckout.Projects.find_one({"projectId":project_id})
    # success, message = usersDB.joinProject(client, userId, projectId)
    if project:
            # client.HardwareCheckout.Projects.update_one({"projectId": ObjectId(project_id)}, {"$addToSet": {"users": user_id}})
            result = db.Projects.update_one(
                {'projectId': project_id},
                {'$push': {'users': user_id}}
            )
            client.close()
            return jsonify(success=True)
    else:
        client.close()
        return jsonify(success=False, message="Project not found"), 404

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



@app.route('/check_out', methods=['POST'])
def check_out():
    projectId = request.json.get('projectId')
    hwSetName = request.json.get('hwSetName')

    client = MongoClient(MONGODB_SERVER)
    projectsDB.checkOutHW(client, projectId, hwSetName)
    client.close()

    return jsonify({'success': True, 'message': 'Checked in ' + hwSetName})


@app.route('/check_in', methods=['POST'])
def check_in():
    projectId = request.json.get('projectId')
    hwSetName = request.json.get('hwSetName')

    client = MongoClient(MONGODB_SERVER)
    projectsDB.checkInHW(client, projectId, hwSetName)
    client.close()

    return jsonify({'success': True, 'message': 'Checked out ' + hwSetName})


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