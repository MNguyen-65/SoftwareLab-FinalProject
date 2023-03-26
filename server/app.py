from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

import usersDB
import projectsDB
import hardwareDB

app = Flask(__name__)

'''
Structure of User entry so far:
User = {
    "username": username,
    "userid": userid,
    "password": password,
    "projects": [project1, ...]
}
'''
# Function tries to login a user with their provided username and Password
# Returns json specfiying if the user login attempt was successful or not
@app.route('/login', methods=['POST'])
def login():
    # print("Attempting login")
    username = request.json.get('username')
    userid = request.json.get('userid')
    password = request.json.get('password')

    success, message = usersDB.login(username, userid, password)

    return jsonify({'success': success, 'message': message})


# Function tries to create a user with their provided username and Password
# Returns json specfiying if the user creation was successful or not
@app.route('/add_user', methods=['POST'])
def add_user():
    # print(f"Attempting AddUser {request.json}")
    username = request.json.get('username')
    userid = request.json.get('userid')
    password = request.json.get('password')

    success, message = usersDB.addUser(username, userid, password)

    return jsonify({'success': success, 'message': message})


@app.route('/get_projects', methods=['GET'])
def get_projects():
    username = request.json.get('username')
    client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")

    user = client.HardwareCheckout.People.find_one({'username': username})
    projects = user['projects']

    return jsonify(projects)



'''
Structure of Project entry so far:
Project = {
    "name": projectName,
    "projectid": projectID,
    "description": description
    "users": [user1, user2, ...]
    "hwsets": {'HW1': 0, 'HW2': 10, ...}
    # Should probably be a map with HWSetName and amount used by this project
}
'''


@app.route('/add_project', methods=['POST'])
def add_project():
    projectName = request.json.get('name')
    projectID = request.json.get('projectid')
    description = request.json.get('description')

    success, message = projectsDB.addProject(projectName, projectID, description)

    return jsonify({'success': success, 'message': message})


'''
Structure of Hardware Set entry so far:
HardwareSet = {
    "Name": hwSetName,
    "Capacity": initialCapacity,
    "Availability": initialCapacity
}
'''

@app.route('/add_hardware', methods=['POST'])
def add_hardware_set():
    hwSetName = request.json.get('Name')
    initCapacity = request.json.get('initCapacity')

    db = mongo.HardwareCheckout
    hwsets = db.HardwareSets
    
    doc = {
        "Name": hwSetName,
        "Capacity": str(initCapacity),
        "Availability": str(initCapacity)
    }

    hwsets.insert_one(doc)

@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    print("testing check inv")
    client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")

    projects = []
    for project in client.HardwareCheckout.Projects.find():
        projects.append({
            'name': project['name'],
            'projectid': project['projectid'],
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
    
    # Check if the user exists in the database
    user = mongo.HardwareCheckout.People.find_one({'username': username})
    if not user:
        return jsonify({'success': False, 'message': 'username invalid. Unable to check in item'})

    # Update the inventory of the checked in item
    item = mongo.HardwareCheckout.HardwareSets.find_one({'Name': hardwareItem})
    # If item doesn't already exist in inventory, create it and intialize capacity and available values to quantity provided
    if not item:
        item = {'Name': hardwareItem, 'Available': quantity, 'Capacity': quantity}
        mongo.HardwareCheckout.HardwareSets.insert_one(item)
    # Item exists; update availability
    else:
        item['Available'] += quantity
        mongo.HardwareCheckout.HardwareSets.update_one({'_id': item['_id']}, {'$set': {'Available': item['Available']}})

    # Update the user's data
    if hardwareItem not in user['Items']:
        user['Items'][item_name] = quantity
    else:
        user['Items'][item_name] += quantity
    mongo.HardwareCheckout.People.update_one({'_id': user['_id']}, {'$set': {'Items': user['Items']}})

    # return json success message
    return jsonify({'success': True, 'message': f'Item {hardwareItem} checked in successfully.'})


@app.route('/check_out', methods=['POST'])
def check_out():
    username = request.json.get('username')
    hardwareItem = request.json.get('HardwareItem')
    quantity = request.json.get('quantity')

    # Check if the user exists in the database
    user = mongo.HardwareCheckout.People.find_one({'username': username})
    if not user:
        return jsonify({'success': False, 'message': 'username invalid. Unable to check in item'})

    # Check if the item exists in the inventory
    item = mongo.HardwareCheckout.HardwareSets.find_one({'Name': hardwareItem})
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
    
    mongo.db.inventory.update_one({'_id': item['_id']}, {'$set': {'quantity': item['quantity']}})

    # Update the user's data
    user['Items'][hardwareItem] -= quantity

    # mongo.HardwareCheckout.HardwareSets refers to the HardwareSets collection in the mongoDB
    mongo.HardwareCheckout.HardwareSets.update_one({'_id': item['_id']}, {'$set': {'Available': item['Available']}})
    mongo.HardwareCheckout.People.update_one({'_id': user['_id']}, {'$set': {'Items': user['Items']}})

    return jsonify({'success': True, 'message': 'Item checked out successfully.'})

if __name__ == '__main__':
    app.run()