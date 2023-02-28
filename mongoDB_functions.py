# TODO: add delete_item() method
# TODO: add timestamps, track ordering of people

from pymongo import MongoClient

client = MongoClient("mongodb+srv://goblin:Password1234@database.kbcy6ct.mongodb.net/test")
db = client.HardwareCheckout # main database where we have people, hardware, and projects
hardwareCollection = db.HardwareSet  # hardwareCollection is the collection for hardware

# initializing a new item with a quantity
# future to-do: check that item not already in database
def create_new_item(name, qty):
    post = {
        "Item": name,
        "Capacity": qty,
        "Available": qty
    }
    post_id = hardwareCollection.insert_one(post).inserted_id
    print(post)

# adding more available quantity to an item
def add_qty_to_item(name, qty):
    # fetch document to find existing capacity and availability
    item = hardwareCollection.find({ "Item": name })

    new_qty = item.Available
    new_cap = item.Capacity

    item_document = { "Item": name }
    new_qty = { "$set": { "Available": str(new_qty) , "Capacity" : str(new_qty) } }
    hardwareCollection.update_one(item_document, new_qty)



# a person wants to checkout an item
def checkout_item(name, item, qty):
    return

# a person wants to return an item
def return_item(name, item, qty):
    return

create_new_item("robot", 10)
create_new_item("goo", 90)
