import base64
import copy
import json

import pytest

from todos.app import app
from todos.helpers import BASE_URL, TODOS


def test_get_all_todos():
    with app.test_client() as client:
        response = client.get(
            '{}/todos'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin')
            }
        )
        data_response = json.loads(response.data)

        expected_data = {
            'todos': TODOS
        }

        assert response.status_code == 200
        assert data_response == expected_data


def test_get_todo_by_id():
    with app.test_client() as client:
        response = client.get(
            '{}/todos/1'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin')
            }
        )
        data_response = json.loads(response.data)

        expected_data = {
            'todo': TODOS[0]
        }

        assert response.status_code == 200
        assert data_response == expected_data


def test_update_todo_by_id():
    with app.test_client() as client:

        assert TODOS[0]['status'] == 'pending'

        response = client.put(
            '{}/todos/1'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin'),
                'Content-Type': 'application/json',
            },
            data=json.dumps({
                "status": "completed",
                "title": "Packing"
            })
        )

        assert response.status_code == 200
        assert TODOS[0]['status'] == 'completed'


def test_update_todo_with_wrong_status_name():
    with app.test_client() as client:

        response = client.put(
            '{}/todos/1'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin'),
                'Content-Type': 'application/json',
            },
            data=json.dumps({
                "status": "done",
                "title": "Packing"
            })
        )
        data_response = json.loads(response.data)

        expected_response = {
            'error': 'Method not allowed because of a missing title or a missing json, or wrong status name (valid: competed, pending)'
        }

        assert response.status_code == 400
        assert data_response == expected_response


def test_delete_todo_by_id():
    with app.test_client() as client:

        TEST_TODOS = copy.deepcopy(TODOS)

        assert len(TODOS) == 2
        assert TODOS == TEST_TODOS

        response = client.delete(
            '{}/todos/1'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin')
            }
        )

        assert response.status_code == 200
        assert len(TODOS) == 1
        assert TODOS == [TEST_TODOS[1]]



def test_create_todo():
    with app.test_client() as client:

        TEST_TODOS = copy.deepcopy(TODOS)

        assert len(TODOS) == 1
        assert TODOS == TEST_TODOS

        response = client.post(
            '{}/todos'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin'),
                'Content-Type': 'application/json',
            },
            data=json.dumps({
                "date": "2018-03-15",
                "description": "Traveling to visit my parents",
                "title": "Traveling"
            })
        )

        expected_data = {
            'date': '2018-03-15',
            'description': 'Traveling to visit my parents', 
            'id': 3,
            'status': 'pending',
            'title': 'Traveling'
        }

        assert response.status_code == 201
        assert len(TODOS) == 2
        assert TODOS[1] == expected_data


@pytest.mark.parametrize('test_data', [
    {"date": "2018-03-15"},  # Missing title
    None  # Missing json
])
def test_create_todo_with_wrong_data(test_data):
  with app.test_client() as client:

        response = client.post(
            '{}/todos'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode('jamie:admin'),
                'Content-Type': 'application/json',
            },
            data=json.dumps(test_data)
        )
        data_response = json.loads(response.data)

        expected_response = {
            'error': 'Method not allowed because of a missing title or a missing json, or wrong status name (valid: competed, pending)'
        }

        assert response.status_code == 400
        assert data_response == expected_response


def test_unauthorized_request():
    with app.test_client() as client:
        response = client.get(
            '{}/todos'.format(BASE_URL),
            headers={
                'Authorization': 'Basic ' + base64.b64encode(':')
            }
        )
        data_response = json.loads(response.data)

        expected_response = {
            'error': 'Unauthorized access'
        }

        assert response.status_code == 401
        assert data_response == expected_response
