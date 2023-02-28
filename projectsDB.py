from pymongo import MongoClient

def addProject(projectName, projectID, description):
    client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")
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
def queryProject(projectName):
    client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/?retryWrites=true&w=majority")
    db = client.HardwareCheckout
    projects = db.Projects

    query = {"Name": projectName}
    doc = projects.find_one(query)
    client.close()

    return doc