import pytest
import os
import pymongo
import mongomock
import todo_app.app
from datetime import datetime,timedelta
from dotenv import load_dotenv, find_dotenv
from unittest.mock import patch

file_path = find_dotenv('.env.test')
load_dotenv(file_path, override=True)

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test') 
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=((os.getenv('MONGO_URL'), 27017),)):
        test_app = todo_app.app.create_app()
        test_app.config['LOGIN_DISABLED'] = True

        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<h3 class="border-bottom border-gray pb-2 mb-0">To Do</h3>' in response.data
    assert b'<h3 class="border-bottom border-gray pb-2 mb-0">Doing</h3>' in response.data
    assert b'<h3 class="border-bottom border-gray pb-2 mb-0">Done</h3>' in response.data

@mongomock.patch(servers=((os.getenv('MONGO_URL'), 27017),))
def test_add_item():
    mockclient = pymongo.MongoClient(f"{os.environ.get('MONGO_PROTOCOL')}://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_URL')}")

    db = mockclient[os.environ.get('MONGO_DATABASE')]

    mock_list_id = db.lists.insert_one({"name": "Test List"}).inserted_id
    
    db.cards.insert_one({"dateLastActivity": datetime.utcnow(),"desc": 'To Do item',"idList": mock_list_id,"name": 'To Do', "due": (datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y")})
    db.cards.insert_one({"dateLastActivity": datetime.utcnow(),"desc": 'Doing item',"idList": mock_list_id,"name": 'Doing', "due": (datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y")})
    db.cards.insert_one({"dateLastActivity": datetime.utcnow(),"desc": 'Done item',"idList": mock_list_id,"name": 'Done', "due": (datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y")})
