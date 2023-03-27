from pymongo import MongoClient

MONGODB_SERVER = 'mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority'

'''
Structure of Hardware Set entry so far:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initialCapacity,
    'availability': initialCapacity
}
'''

def addHardwareSet(hwSetName, initCapacity):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    hwsets = db.HardwareSets
    
    if not hwsets.find({'hwName': hwSetName}):
        doc = {
            'hwName': hwSetName,
            'capacity': str(initCapacity),
            'availability': str(initCapacity)
        }
        hwsets.insert_one(doc)
        
        success = True
        message = 'Successfully added hardware set'
    else:
        success = False
        message = 'Name already taken by another hardware set'

    client.close()

    return success, message

# Might have to be private
def queryHardwareSet(hwSetName):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    hwsets = db.HardwareSets

    query = {'hwName': hwSetName}
    doc = hwsets.find_one(query)
    client.close()

    return doc

def updateAvailability(hwSetName, newAvailability):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    hwsets = db.HardwareSets

    filter = {'hwName': hwSetName}
    newValue = {'$set': {'availability': newAvailability}}

    hwsets.update_one(filter, newValue)
    client.close()

def checkOut(hwSetName):
    return

def checkIn(hwSetName):
    return

def requestSpace(hwSetName, amount):
    hwset = queryHardwareSet(hwSetName)
    avail = int(hwset['Availability'])
    allocated = min(avail, amount)
    avail -= allocated

    # Change database entry
    updateAvailability(hwSetName, avail)

    return allocated