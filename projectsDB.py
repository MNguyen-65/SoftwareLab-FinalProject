from pymongo import MongoClient

MONGODB_SERVER = "mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority"

'''
Structure of Project entry so far:
Project = {
    "Name": projectName,
    "ProjectID": projectID,
    "Description": description
    "HardwareSets": [HW1_ID, HW2_ID, ...]
}
'''

def addProject(projectName, projectID, description):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects
    # Should check if projectName & projectID are unique
    
    # Keep track of HW sets for this project
    doc = {
        "Name": projectName,
        "ProjectID": projectID,
        "Description": description
    }

    projects.insert_one(doc)
    client.close()

# Might have to be private
# Can either query based on project name or ID
def queryProject(projectID):
    client = MongoClient(MONGODB_SERVER)
    db = client.HardwareCheckout
    projects = db.Projects

    query = {"ProjectID": projectID}
    doc = projects.find_one(query)
    client.close()

    return doc