from pymongo import MongoClient

MONGODB_SERVER = "mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority"

'''
Structure of Hardware Set entry so far:
HardwareSet = {
    "Name": hwSetName,
    "Capacity": initialCapacity,
    "Availability": initialCapacity
}
'''

def addHardwareSet(hwSetName, initCapacity):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    hwsets = db.HardwareSets
    
    doc = {
        "Name": hwSetName,
        "Capacity": str(initCapacity),
        "Availability": str(initCapacity)
    }

    hwsets.insert_one(doc)
    client.close()

# Might have to be private
def queryHardwareSet(hwSetName):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    hwsets = db.HardwareSets

    query = {"Name": hwSetName}
    doc = hwsets.find_one(query)
    client.close()

    return doc
