""" The authentication module """
import json
from crypt import crypt
from flask import request, Blueprint, make_response
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultsFound
from flask_login import login_user
from models import User, get_session

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route('/login', methods=['POST'])
def login():
    body = request.json
    received_user_email = body['email']
    session = get_session()
    try:
        user = session.query(User).filter_by(
            User.email == str(received_user_email)
        ).one()
    except (MultipleResultsFound, NoResultsFound):
        return make_response(401, json.dumps(
                {'error': 401, 'message': 'unauthorized'}
            )
        )

    salt = user.password.split("$")[2]
    received_password = crypt(body['password'], salt)

    if received_password == user.password:
        login_user(user)
        return make_response(200, json.dumps(
                {'error': False, 'message': 'authorized'}
            )
        )
