from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

import usersDB
import projectsDB
import hardwareDB

app = Flask(__name__)


# Function tries to login a user with their provided username and Password
# Returns json specfiying if the user login attempt was successful or not
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username') # username, password are taken in from the webpage html
    userId = request.json.get('userId')
    password = request.json.get('password')

    success, message = usersDB.login(username, userId, password)

    return jsonify({'success': success, 'message': message})


# Function tries to create a user with their provided username and Password
# Returns json specfiying if the user creation was successful or not
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.json.get('Username')
    userId = request.json.get('userId')
    password = request.json.get('Password')

    success, message = usersDB.addUser(username, userId, password)

    return jsonify({'success': success, 'message': message})


@app.route('/create_project', methods=['POST'])
def create_project():
    userId = request.json.get('userId')
    projectName = request.json.get('projectName')
    projectId = request.json.get('projectId')
    description = request.json.get('description')

    success, message = projectsDB.createProject(projectName, projectId, description)
    if not success:
        return jsonify({'success': success, 'message': message})
    
    success, message = usersDB.joinProject(userId, projectId)
    return jsonify({'success': success, 'message': message})


@app.route('/join_project', methods=['POST'])
def join_project():
    userId = request.json.get('userId')
    projectId = request.json.get('projectId')
    
    success, message = usersDB.joinProject(userId, projectId)
    return jsonify({'success': success, 'message': message})


@app.route('/add_project', methods=['POST'])
def add_project():
    projectName = request.json.get('name')
    projectId = request.json.get('projectId')
    description = request.json.get('description')

    success, message = projectsDB.addProject(projectName, projectId, description)

    return jsonify({'success': success, 'message': message})


@app.route('/add_hardware', methods=['POST'])
def add_hardware_set():
    hwSetName = request.json.get('name')
    initCapacity = request.json.get('initCapacity')

    client = MongoClient('mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority')

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
    client = MongoClient('mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority')

    projects = []
    for project in client.HardwareCheckout.Projects.find():
        projects.append({
            'name': project['name'],
            'projectId': project['projectId'],
            'description': project['description']
            
            # add more fields as needed
        })
    return jsonify(projects)

# Function tries to create a user with their provided username and Password
# Returns json specfiying if the user creation was successful or not
@app.route('/check_in', methods=['POST'])
def check_in():
    username = request.json.get('username')
    hardwareItem = request.json.get('HardwareItem')
    quantity = request.json.get('quantity')

    client = MongoClient('mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority')

    
    # Check if the user exists in the database
    user = client.HardwareCheckout.Users.find_one({'username': username})
    if not user:
        return jsonify({'success': False, 'message': 'username invalid. Unable to check in item'})

    # Update the inventory of the checked in item
    item = client.HardwareCheckout.HardwareSets.find_one({'Name': hardwareItem})
    # If item doesn't already exist in inventory, create it and intialize capacity and available values to quantity provided
    if not item:
        item = {'Name': hardwareItem, 'Available': quantity, 'Capacity': quantity}
        client.HardwareCheckout.HardwareSets.insert_one(item)
    # Item exists; update availability
    else:
        item['Available'] += quantity
        client.HardwareCheckout.HardwareSets.update_one({'_id': item['_id']}, {'$set': {'Available': item['Available']}})

    # Update the user's data
    if hardwareItem not in user['Items']:
        user['Items']['item_name'] = quantity
    else:
        user['Items']['item_name'] += quantity
    client.HardwareCheckout.Users.update_one({'_id': user['_id']}, {'$set': {'Items': user['Items']}})

    # return json success message
    return jsonify({'success': True, 'message': f'Item {hardwareItem} checked in successfully.'})


@app.route('/check_out', methods=['POST'])
def check_out():
    username = request.json.get('username')
    hardwareItem = request.json.get('HardwareItem')
    quantity = request.json.get('quantity')

    client = MongoClient('mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority')

    # Check if the user exists in the database
    user = client.HardwareCheckout.Users.find_one({'username': username})
    if not user:
        return jsonify({'success': False, 'message': 'username invalid. Unable to check in item'})

    # Check if the item exists in the inventory
    item = client.HardwareCheckout.HardwareSets.find_one({'Name': hardwareItem})
    if not item:
        return jsonify({'success': False, 'message': 'Item not found.'})

    # Check if enough of the item is available
    if quantity > user['Available']:
        return jsonify({'success': False, 'message': f'Not enough quantity of {hardwareItem} available'})

    # Checkout the item and update the inventory
    item['quantity'] -= quantity

    # Add the quantity of hardwareItem to the user's profile
    if hardwareItem in user['Items']:
        user['Items'][hardwareItem]+= quantity
    else:
        user['Items'][hardwareItem]= quantity # if the tool isn't in the user's profile, add it to the dictionary
    
    client.db.inventory.update_one({'_id': item['_id']}, {'$set': {'quantity': item['quantity']}})

    # Update the user's data
    user['Items'][hardwareItem] -= quantity

    # client.HardwareCheckout.HardwareSets refers to the HardwareSets collection in the mongoDB
    client.HardwareCheckout.HardwareSets.update_one({'_id': item['_id']}, {'$set': {'Available': item['Available']}})
    client.HardwareCheckout.Users.update_one({'_id': user['_id']}, {'$set': {'Items': user['Items']}})

    return jsonify({'success': True, 'message': 'Item checked out successfully.'})


if __name__ == '__main__':
    app.run()