#!flask/bin/python
from flask import abort, Blueprint, Flask, jsonify, make_response, request

from helpers import check_authorization, TODOS


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def method_not_allowed(error):
    return make_response(jsonify(
        {'error': 'Method not allowed because of a missing title or a missing json, or wrong status name (valid: competed, pending)'}),
        400
    )


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def todo():
    return "Hello Jamie on your TODO list page!"


@app.route('/todos', methods=['GET'])
def get_all_todos():
    check_authorization(request.authorization["username"], request.authorization["password"])
    return jsonify({'todos': TODOS})


@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_todo_by_id(todo_id):
    check_authorization(request.authorization["username"], request.authorization["password"])
    todo = [(idx, todo) for idx, todo in enumerate(TODOS) if todo['id'] == todo_id]
    todo_idx, todo = todo[0][0], todo[0][1]
    print(todo)
    if len(todo) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify({'todo': todo})

    elif request.method == 'PUT':
        if not request.json:
            abort(400)
        status = request.json.get('status', None)
        if status and status not in ('completed', 'pending'):
            abort(400)
        todo['date'] = request.json.get('date', todo['date'])
        todo['description'] = request.json.get('description', todo['description'])
        todo['status'] = request.json.get('status', todo['status'])
        todo['title'] = request.json.get('title', todo['title'])
        return jsonify({'todo': todo})

    elif request.method == 'DELETE':
        todo_title = todo['title']
        del TODOS[todo_idx]
        return jsonify({'message': 'Successfully removed {} from TODOS'.format(todo_title)})


@app.route('/todos', methods=['POST'])
def create_todo():
    check_authorization(request.authorization["username"], request.authorization["password"])
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'date': request.json.get('date', None),
        'description': request.json.get('description', None),
        'id': TODOS[-1]['id'] + 1,
        'status': 'pending',
        'title': request.json['title']
    }
    TODOS.append(todo)
    return jsonify({'todo': todo}), 201


if __name__ == '__main__':
    app.run(debug=True)
