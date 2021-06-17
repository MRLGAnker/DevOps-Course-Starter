import pytest
import os
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from unittest.mock import Mock, patch

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    mock_get_requests.side_effect = mock_request
    response = client.get('/')

    assert response.status_code == 200
    assert b'To Do Item' in response.data
    assert b'Doing Item' in response.data
    assert b'Test Done Item' in response.data
	 
def mock_request(url,params):
    if url.startswith(f"https://api.trello.com/1/boards/{os.environ.get('BOARD_ID')}/lists"):
        response = Mock()

        json_return = [
            {
                "id": "987",
                "name": "To Do"
            },
            {
                "id": "876",
                "name": "Doing"
            },
            {
                "id": "765",
                "name": "Done"
            }
        ]
        response.json.return_value = json_return
        return response
    
    elif url.startswith(f"https://api.trello.com/1/boards/{os.environ.get('BOARD_ID')}/cards"):
        response = Mock()

        json_return = [
            {
                "id": "123",
                "dateLastActivity": "2021-04-11T17:10:36.263Z",
                "desc": "Test To Do Item",
                "idBoard": "B04RD",
                "idList": "987",
                "name": "To Do Item",
                "due": None
            },
            {
                "id": "234",
                "dateLastActivity": "2021-04-20T06:11:36.345Z",
                "desc": "Test Doing Item",
                "idBoard": "B04RD",
                "idList": "876",
                "name": "Doing Item",
                "due": "2021-04-28T00:00:00.000Z"
            },
            {
                "id": "345",
                "dateLastActivity": "2021-05-01T12:43:36.286Z",
                "desc": "Test Done Item",
                "idBoard": "B04RD",
                "idList": "765",
                "name": "Done Item",
                "due": "2021-05-05T00:00:00.000Z"
            }
        ]
        response.json.return_value = json_return
        return response
    return None