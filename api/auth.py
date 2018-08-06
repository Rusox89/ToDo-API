""" The authentication module """
import json
from crypt import crypt
from flask import request, Blueprint, make_response, abort
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask_login import login_user
from api.models import User, get_session

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route('/login', methods=['POST'])
def login():
    body = request.json
    received_user_email = body['email']
    if not (isinstance(body['email'], str) and isinstance(body['password'], str)):
        abort(400)
    session = get_session()
    try:
        user = session.query(User).filter(
            User.email == str(received_user_email)
        ).one()
    except (MultipleResultsFound, NoResultFound):
        return make_response(json.dumps(
                {'error': 401, 'message': 'unauthorized'}
            ), 401
        )

    salt = user.password.split("$")[2]
    print(salt)
    print(user.password)
    received_password = crypt(body['password'], salt)

    if received_password == user.password:
        login_user(user)
        return make_response(json.dumps(
                {'error': False, 'message': 'authorized'}
            ), 200
        )
    else:
        return make_response(json.dumps(
                {'error': 401, 'message': 'unauthorized'}
            ), 401
        )
