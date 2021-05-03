from logging import Formatter
import os
import requests
from datetime import date, datetime
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
            self.due = self.due = datetime.strptime(due,'%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            self.due = None
        self.dateLastActivity = datetime.strptime(dateLastActivity,'%Y-%m-%dT%H:%M:%S.%fZ')

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
    def show_all_done_items(self):
        if len(self.done_items) < 5:
            return True
        else:
            return False

    @property
    def recent_done_items(self):
        list_id = search_list(self._lists,'Done')
        done_items = [item for item in self._items if item.idList == search_list(self._lists,'Done')]
        return [item for item in done_items if item.dateLastActivity.date() == datetime.utcnow().date()]

    @property
    def older_done_items(self):
        done_items = [item for item in self._items if item.idList == search_list(self._lists,'Done')]
        return [item for item in done_items if item.dateLastActivity.date() < datetime.utcnow().date()]

def get_auth_params():
    """
    Returns authentication parameters.

    Returns:
        Authentication parameters in JSON format.
    """
    return {'key': os.environ.get('SECRET_KEY'),'token': os.environ.get('SECRET_TOKEN')}

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

def get_lists():
    """
    Fetches all Lists from the given Trello Board.

    Returns:
        JSON response.
    """
    lists = []

    for list in (requests.get(f"https://api.trello.com/1/boards/{os.environ.get('BOARD_ID')}/lists",params=get_auth_params())).json():
        lists.append(List(list['id'],list['name']))

    return lists

def get_cards():
    """
    Fetches all Cards from the given Trello Board.

    Returns:
        JSON response.
    """
    cards = []
    today = datetime.today().date()

    for card in (requests.get(f"https://api.trello.com/1/boards/{os.environ.get('BOARD_ID')}/cards",params=get_auth_params())).json():
        cards.append(Card(card['id'],card['name'],card['idList'],card['desc'],card['due'],card['dateLastActivity']))

    return cards

def create_card(name,list_id):
    """
    Creates a card with the given name and Trello List.

    Returns:
        JSON response.
    """
    post = requests.post(f"https://api.trello.com/1/cards?name={name}&idList={list_id}",params=get_auth_params())
    
    response_json = post.json()

    return response_json

def move_card(card_id,list_id):
    """
    Moves an item to the given Trello List.

    Returns:
        JSON response.
    """
    put = requests.put(f"https://api.trello.com/1/cards/{card_id}?idList={list_id}",params=get_auth_params())
    
    response_json = put.json()

    return response_json

def remove_card(card_id):
    """
    Moves an item to the given Trello List.

    Returns:
        JSON response.
    """
    post = requests.delete(f"https://api.trello.com/1/cards/{card_id}",params=get_auth_params())
    
    response_json = post.json()

    return response_json


def create_board(name):
    """
    Creates a Trello Board.

    Returns:
        JSON response.
    """
    post = requests.post(f"https://api.trello.com/1/boards/?name={name}",params=get_auth_params())
    
    response_json = post.json()

    return response_json

def delete_board(board_id):
    """
    Deletes a Trello Board.

    Returns:
        JSON response.
    """
    put = requests.delete(f"https://api.trello.com/1/boards/{board_id}",params=get_auth_params())
    
    response_json = put.json()

    return response_json