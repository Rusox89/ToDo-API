""" The authentication module """
import json
import logging
from crypt import crypt
from flask import request, Blueprint, make_response, abort
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from api.models import User, get_session

auth = Blueprint("auth", __name__, url_prefix="/auth")
login_manager = LoginManager()

logging.basicConfig(level=logging.DEBUG)

@login_manager.user_loader
def load_user(user_email):
    logging.debug("Loading user")
    session = get_session()
    user = None
    try:
        user = session.query(User).filter(User.email == user_email).one()
        logging.debug("User loaded")
        
    except (MultipleResultsFound, NoResultFound):
        logging.debug("No user found with id {}".format(str(uid)))

    session.close()
    return user

@auth.route('/login', methods=['POST'])
def login():
    logging.debug("Logging in")
    body = request.json
    received_user_email = body['email']
    if not (isinstance(body['email'], str) and isinstance(body['password'], str)):
        abort(400)

    session = get_session()

    try:
        user = session.query(User).filter(
            User.email == str(received_user_email)
        ).one()

        received_password = crypt(body['password'], user.password)

        if received_password == user.password:
            login_user(user)
            response = make_response(json.dumps(
                    {'error': False, 'message': 'authorized'}
                ), 200
            )
        else:
            response = make_response(json.dumps(
                    {'error': 401, 'message': 'unauthorized'}
                ), 401
            )

    except (MultipleResultsFound, NoResultFound):
        response = make_response(json.dumps(
                {'error': 401, 'message': 'unauthorized'}
            ), 401
        )
    session.close()
    return response


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    """ Logout the user. """
    logout_user()
    return make_response(
            json.dumps(
                {'error': 200, 'message': 'logged_out'}
            ), 200
        )
