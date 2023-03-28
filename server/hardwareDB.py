from pymongo import MongoClient

'''
Structure of Hardware Set entry so far:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

def addHardwareSet(client, hwSetName, initCapacity):
    hwsets = client.HardwareCheckout.HardwareSets
    
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


    return success, message


def queryHardwareSet(client, hwSetName):
    hwsets = client.HardwareCheckout.HardwareSets

    query = {'hwName': hwSetName}
    doc = hwsets.find_one(query)

    return doc


def updateAvailability(client, hwSetName, newAvailability):
    hwsets = client.HardwareCheckout.HardwareSets

    filter = {'hwName': hwSetName}
    newValue = {'$set': {'availability': newAvailability}}

    hwsets.update_one(filter, newValue)


def requestSpace(client, hwSetName, amount):
    hwset = queryHardwareSet(hwSetName)
    avail = int(hwset['availability'])
    if amount > avail:
        return False, 'Not enough space available'
    
    avail -= amount
    updateAvailability(client, hwSetName, avail)

    return True, 'Successfully requested space'


def checkOut(client, hwSetName):
    return


def checkIn(client, hwSetName, amount):
    hwset = queryHardwareSet(hwSetName)
    updateAvailability(client, hwSetName, int(hwset['availability']) + amount)
    return True, 'Successfully checked out hardware'
