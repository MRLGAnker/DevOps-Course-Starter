import pytest
import os
import pymongo
import mongomock
import todo_app.app
from datetime import datetime,timedelta
from dotenv import load_dotenv, find_dotenv
from unittest.mock import patch

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

    #assert response.status_code == 200
    assert b'To Do Item' in response.data
    assert b'Doing Item' in response.data
    assert b'Test Done Item' in response.data

@mongomock.patch(servers=((os.getenv('MONGO_URL'), 27017),))
def test_add_item():
    mockclient = pymongo.MongoClient(f"mongodb://{os.environ.get('MONGO_URL')}")

    db = mockclient[os.environ.get('MONGO_NAMESPACE')]

    mock_list_id = db.lists.insert_one({"name": "Test List"}).inserted_id
    
    db.cards.insert_one({"dateLastActivity": datetime.utcnow(),"desc": 'To Do item',"idList": mock_list_id,"name": 'To Do', "due": (datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y")})
    db.cards.insert_one({"dateLastActivity": datetime.utcnow(),"desc": 'Doing item',"idList": mock_list_id,"name": 'Doing', "due": (datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y")})
    db.cards.insert_one({"dateLastActivity": datetime.utcnow(),"desc": 'Done item',"idList": mock_list_id,"name": 'Done', "due": (datetime.utcnow() + timedelta(days=2)).strftime("%m/%d/%Y")})
