from pymongo import MongoClient

'''
Structure of Hardware Set entry so far:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

def createHardwareSet(client, hwSetName, initCapacity):
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
    hwset = queryHardwareSet(client, hwSetName)
    if hwset == None:
        return False, 'Hardware set does not exist'
    avail = int(hwset['availability'])
    if amount > avail:
        return False, 'Not enough hardware available'
    
    avail -= amount
    updateAvailability(client, hwSetName, avail)

    return True, 'Successfully requested ' + str(amount) + ' hardware.\n' + str(hwSetName) + ': ' + str(avail) + '/' + str(hwset['capacity'])


def getAllHwNames(client):
    hwsets = client.HardwareCheckout.HardwareSets
    hwlist = list(hwsets.find({}))
    hwNames = []
    for hw in hwlist:
        hwNames.append(hw['hwName'])

    return hwNames
