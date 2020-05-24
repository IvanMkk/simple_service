from bottle import run, route, request, abort, response
from marshmallow import Schema, fields, validate
import copy
import uuid

user_data = {}


class user(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    age = fields.Int(required=True, validate=validate.Range(min=0, max=99))


@route('/user', method='POST')
def user_create():
    # creating user via json input data.
    # json {
    #   name: str, len 3-30
    #   age: int, range 0-99
    # }

    request_data = copy.deepcopy(request.json)
    if not request_data:
        abort(400, f"""Not valid input data. \n\
            Expecting json {{name: str(3-30), age: int(0-99)}}.""")

    request_data['id'] = str(uuid.uuid1())

    try:
        user_data[request_data['id']] = user().load(request_data)
        # user created successfully 201
        response.status = 201
        return request_data['id']
    except Exception as e:
        print(e)
        # user creation problems 400
        abort(400, f"""Not valid input data. \n\
            Expecting json {{name: str(3-30), age: int(0-99)}}.
            Got {request.json}""")


@route('/user/<id>', method='DELETE')
def user_delete(id):
    if id in user_data:
        # user found 204
        del user_data[id]
        response.status = 204
    else:
        # user not found 404
        abort(404, "Sorry, user cant be found")


@route('/user/<id>')
def get_user_by_id(id):
    if id in user_data:
        # user found 200
        response.status = 200
        return user_data[id]
    else:
        # user not found 404
        abort(404, "Sorry, user cant be found")


@route('/users')
def get_all_users():
    # user found 200
    return user_data


if __name__ == '__main__':
    run(debug=True, reloader=True)
