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
        try:
            self.due = datetime.strptime(due,'%d/%m/%Y')
        except:
            self.due = None
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

def connect_db():
    client = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_URL')}/{os.environ.get('MONGO_DATABASE')}?w=majority")
    db = client[os.environ.get('MONGO_NAMESPACE')]
    return db

def get_lists():
    """
    Fetches all Lists from the given Trello Board.

    Returns:
        JSON response.
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
    Fetches all Lists from the given Trello Board.

    Returns:
        JSON response.
    """
    cards = []

    for card in connect_db().cards.find({}):
        cards.append(Card(card['_id'],card['name'],card['idList'],card['desc'],card['due'],card['dateLastActivity']))

    return cards

def create_card(desc,list_id,name,due):
    """
    Creates a card with the given name and Trello List.

    Returns:
        JSON response.
    """
    card = {"dateLastActivity": datetime.utcnow(),"desc": desc,"idList": ObjectId(list_id),"name": name,"due": due}
    return connect_db().cards.insert_one(card)

def move_card(card_id,list_id):
    """
    Moves an item to the given Trello List.

    Returns:
        JSON response.
    """
    return connect_db().cards.update_one({"_id": ObjectId(card_id)},{ "$set": {"idList" : ObjectId(list_id)}})

def remove_card(card_id):
    """
    Removes a card with the given card id.

    Returns:
        JSON response.
    """
    return connect_db().cards.delete_one({"_id": ObjectId(card_id)})

def create_board(name):
    """
    Creates a Trello Board.
    """
    client = pymongo.MongoClient(f"mongodb://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_URL')}/{os.environ.get('MONGO_DATABASE')}?w=majority")
    db = client[name]
    return db

def delete_board(name):
    """
    Deletes a Trello Board.
    """
    client = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_URL')}/{os.environ.get('MONGO_DATABASE')}?w=majority")
    client.drop_database(name)