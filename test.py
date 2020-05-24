import requests
import json


def test_user_create_valid_data():
    """
        creating user with valid data
        expecting code 201 and user registered successfully
    """
    print('<---{0:^40s}--->'.format('test_user_create_valid_data'))

    test_data = [
        {'name': 'Ivan', 'age': '30'},
        {'name': 'Ivan', 'age': '99'},
        {'name': 'Ivan', 'age': '0'},
        {'name': 'Iva', 'age': '0'},
        {'name': 'I'*30, 'age': '0'},
    ]

    for tcase in test_data:
        r = requests.post('http://127.0.0.1:8080/user', json=tcase)
        print(r.status_code == 201)

    new_user_id = r.text
    r = requests.get(f'http://127.0.0.1:8080/user/{new_user_id}')
    user_dict = json.loads(r.text)
    print(user_dict['id'] == new_user_id)


def test_user_create_not_valid_data():
    """
        creating user with not valid data
        expecting code 400
    """
    print('<---{0:^40s}--->'.format('test_user_create_not_valid_data'))

    test_data = [
        {'name': 'Ivan', 'age': '320'},
        {'name': 'Ivan', 'age': ''},
        {'name': 'Ivan', 'age': '100'},
        {'name': 'I', 'age': '30'},
        {'name': 'I'*31, 'age': '30'},
        {'name': '', 'age': '30'},
        {'name': 'Ivan'},
        {'age': '30'},
    ]
    for tcase in test_data:
        r = requests.post('http://127.0.0.1:8080/user', json=tcase)
        print(r.status_code == 400)


def test_user_delete_valid_data():
    """
        deleting user with valid data
        expecting code 204
    """
    print('<---{0:^40s}--->'.format('test_user_delete_valid_data'))

    r = requests.post('http://127.0.0.1:8080/user', json={'name': 'Ivan M', 'age': '30'})
    new_user_id = r.text
    r = requests.get(f'http://127.0.0.1:8080/user/{new_user_id}')
    user_dict = json.loads(r.text)
    print(user_dict['id'] == new_user_id)

    r = requests.delete(f'http://127.0.0.1:8080/user/{new_user_id}')
    print(r.status_code == 204)
    r = requests.get(f'http://127.0.0.1:8080/user/{new_user_id}')
    print(r.status_code == 404)


def test_user_delete_not_valid_data():
    """
        deleting user with not valid data
        expecting code 404
    """
    print('<---{0:^40s}--->'.format('test_user_delete_not_valid_data'))

    r = requests.post('http://127.0.0.1:8080/user', json={'name': 'Ivan M', 'age': '30'})
    new_user_id = r.text
    r = requests.get(f'http://127.0.0.1:8080/user/{new_user_id}')
    user_dict = json.loads(r.text)
    print(user_dict['id'] == new_user_id)

    r = requests.delete(f'http://127.0.0.1:8080/user/{new_user_id}21')
    print(r.status_code == 404)

    r = requests.get(f'http://127.0.0.1:8080/user/{new_user_id}')
    print(r.status_code == 200)


test_user_create_valid_data()
test_user_create_not_valid_data()
test_user_delete_valid_data()
test_user_delete_not_valid_data()
