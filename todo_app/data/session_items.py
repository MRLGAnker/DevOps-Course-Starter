from logging import Formatter
import os
import requests
import arrow
from pprint import pp, pprint
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
        if due:
            self.due = arrow.get(due).datetime.strftime('%d %B %Y')
        else:
            self.due = ''

def get_lists():
    """
    Fetches all Lists from the given Trello Board.

    Returns:
        JSON response.
    """
    lists = []

    for list in (requests.get("https://api.trello.com/1/boards/{}/lists?key={}&token={}".format(os.environ.get('BOARD_ID'),os.environ.get('SECRET_KEY'),os.environ.get('SECRET_TOKEN')))).json():
        lists.append(List(list['id'],list['name']))

    return lists

def get_cards():
    """
    Fetches all Cards from the given Trello Board.

    Returns:
        JSON response.
    """
    cards = []

    for card in (requests.get("https://api.trello.com/1/boards/{}/cards?key={}&token={}".format(os.environ.get('BOARD_ID'),os.environ.get('SECRET_KEY'),os.environ.get('SECRET_TOKEN')))).json():
        cards.append(Card(card['id'],card['name'],card['idList'],card['desc'],card['due']))

    return cards

def create_card(name,list_id):
    """
    Creates a card with the given name and Trello List.

    Returns:
        JSON response.
    """
    post = requests.post("https://api.trello.com/1/cards?key={}&token={}&name={}&idList={}".format(os.environ.get('SECRET_KEY'),os.environ.get('SECRET_TOKEN'),name,list_id))
    
    response_json = post.json()

    return response_json

def move_card(card_id,list_id):
    """
    Moves an item to the given Trello List.

    Returns:
        JSON response.
    """
    
    post = requests.put("https://api.trello.com/1/cards/{}?key={}&token={}&idList={}".format(card_id,os.environ.get('SECRET_KEY'),os.environ.get('SECRET_TOKEN'),list_id))
    
    response_json = post.json()

    return response_json

def remove_card(card_id):
    """
    Moves an item to the given Trello List.

    Returns:
        JSON response.
    """
    
    post = requests.delete("https://api.trello.com/1/cards/{}?key={}&token={}".format(card_id,os.environ.get('SECRET_KEY'),os.environ.get('SECRET_TOKEN')))
    
    response_json = post.json()

    return response_json