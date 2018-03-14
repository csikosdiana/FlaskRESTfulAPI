from flask import abort


BASE_URL = 'http://127.0.0.1:5000'


TODOS = [
    {
        'date': '2018-03-17',
        'description': 'Pack all stuffs to be ready for the moving day', 
        'id': 1,
        'status': 'pending',
        'title': 'Packing'
    },
    {
        'date': '2018-03-18',
        'description': 'Buy cinema tickets for the new Death Wish movie',
        'id': 2,
        'status': 'pending',
        'title': 'Buy cinema tickets'
    }
]


def check_authorization(username, password):
    if username == 'jamie' and password == 'admin':
        return
    else:
        return abort(401)
