from logging import Formatter
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class List:  
    def __init__(self, id, name):  
        self.id = id  
        self.name = name

class Card:  
    def __init__(self, id, name, idList, desc, due):  
        self.id = id  
        self.name = name
        self.idList = idList
        self.desc = desc
        try:
            self.due = self.due = datetime.strptime(due,'%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            self.due = None

def get_auth_params():
    """
    Returns authentication parameters.

    Returns:
        Authentication parameters in JSON format.
    """
    return {'key': os.environ.get('SECRET_KEY'),'token': os.environ.get('SECRET_TOKEN')}

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

    for card in (requests.get(f"https://api.trello.com/1/boards/{os.environ.get('BOARD_ID')}/cards",params=get_auth_params())).json():
        cards.append(Card(card['id'],card['name'],card['idList'],card['desc'],card['due']))

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

class ViewModel:
    def __init__(self, lists, cards):
        self._lists = lists
        self._cards = cards
    
    @property
    def lists(self):
        return self._lists
    
    @property
    def cards(self):
        return self._cards