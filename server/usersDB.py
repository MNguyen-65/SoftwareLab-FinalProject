from pymongo import MongoClient

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

'''
Structure of User entry so far:
User = {
    'username': username,
    'userid': userid,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

def addUser(username, userid, password):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    people = db.People

    existing_user = people.find_one({'username': username, 'userid': userid})
    if existing_user == None:
        doc = {
            'username': username,
            'userid': userid,
            'password': password,
            'projects': []
        }

        people.insert_one(doc)
        success = True
        message = 'Successfully added user'
    else:
        success = False
        message = 'Username or ID already taken'
        # u = existing_user['username']
        # uid = existing_user['userid']
        # pa = existing_user['password']
        # print(f'{u}, {uid}, {pa}')
    
    client.close()

    return success, message


def __queryUser(username, userid):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    people = db.People

    query = {'username': username, 'userid': userid}
    doc = people.find_one(query)
    client.close()

    return doc


def login(username, userid, password):
    doc = __queryUser(username, userid)

    # TODO: encrypt password here
    if(doc == None):
        return False, 'Invalid username or ID. Try again'
    elif(doc['password'] == password):
        return True, 'Login successful'
    else:
        return False, 'Invalid password. Try again'

# def addProject(username, userid, projectID):
