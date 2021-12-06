import pymongo
import os
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

class List:
    
    def __init__(self, id, name):  
        self.id = id  
        self.name = name
        
class Card:  
    def __init__(self, id, name, idList, desc, due, dateLastActivity):  
        self.id = id  
        self.name = name
        self.idList = idList
        self.desc = desc
        self.due = due
        self.dateLastActivity = dateLastActivity

class ViewModel:
    def __init__(self, items, lists):
        self._items = items
        self._lists = lists

    @property
    def items(self):
        return self._items
    
    @property
    def lists(self):
        return self._lists
    
    @property
    def to_do_items(self):
        list_id = search_list(self._lists,'To Do')
        return [item for item in self._items if item.idList == list_id]
    
    @property
    def doing_items(self):
        list_id = search_list(self._lists,'Doing')
        return [item for item in self._items if item.idList == list_id]
    
    @property
    def done_items(self):
        list_id = search_list(self._lists,'Done')
        return [item for item in self._items if item.idList == list_id]

    @property
    def recent_done_items(self):
        done_items = [item for item in self._items if item.idList == search_list(self._lists,'Done')]
        return [item for item in done_items if item.dateLastActivity.date() == datetime.utcnow().date()]

    @property
    def older_done_items(self):
        done_items = [item for item in self._items if item.idList == search_list(self._lists,'Done')]
        return [item for item in done_items if item.dateLastActivity.date() < datetime.utcnow().date()]

    @property
    def show_all_done_items(self):
        return len(self.done_items) < 5

def get_connection():
    connection_string = f"mongodb+srv://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_URL')}"
    return connection_string

def get_database():
    db_name = os.getenv('MONGO_DATABASE')
    return db_name

def connect_db():
    connection = get_connection()
    name = get_database()
    client = pymongo.MongoClient(connection)
    db = client[name]
    return db

def check_default_lists():
    """
    Makes sure the 'To Do', 'Doing' & 'Done' lists exist, inserts them if not.
    """
    default_lists = [{'name': 'To Do'},{'name': 'Doing'},{'name': 'Done'}]
    db = connect_db()

    for default_list in default_lists:
        db.lists.update_one(default_list,{"$set": default_list},True)

def get_lists():
    """
    Fetches all lists in the db.

    Returns:
        List of 'List' objects.
    """
    lists = []

    for list in connect_db().lists.find({}):
        lists.append(List(list['_id'],list['name']))

    return lists

def search_list(list,name):
    """
    Searches the given array of lists for the list with the given name.
    (Assumes there is only 1 match, which should be OK for this exercise)

    Returns:
        List ID of the list with matching name.
    """
    for item in list:
        if item.name == name:
            return item.id

def get_cards():
    """
    Fetches all cards in the db.

    Returns:
        List of 'Card' objects.
    """
    cards = []

    for card in connect_db().cards.find({}):
        cards.append(Card(card['_id'],card['name'],card['idList'],card['desc'],card['due'],card['dateLastActivity']))

    return cards

def create_card(desc,list_id,name,due):
    """
    Creates a card with the given name, list_id & due.

    Returns:
        JSON response.
    """
    test = connect_db()
    card = {"dateLastActivity": datetime.utcnow(),"desc": desc,"idList": ObjectId(list_id),"name": name,"due": datetime.strptime(due,'%d/%m/%Y')}
    return test.cards.insert_one(card)

def move_card(card_id,list_id):
    """
    Moves the card with the given card_id to the list with the given list_id.

    Returns:
        JSON response.
    """
    return connect_db().cards.update_one({"_id": ObjectId(card_id)},{ "$set": {"idList" : ObjectId(list_id)}})

def remove_card(card_id):
    """
    Removes a card with the given card_id.

    Returns:
        JSON response.
    """
    return connect_db().cards.delete_one({"_id": ObjectId(card_id)})

def create_board(name):
    """
    Creates a database.
    """
    connection = get_connection()
    client = pymongo.MongoClient(connection)
    db = client[name]

    return db

def delete_board(name):
    """
    Deletes a database.
    """
    connection = get_connection()
    client = pymongo.MongoClient(connection)
    client.drop_database(name)