from flask import Blueprint, abort, make_response, request
from flask_login import current_user, login_required
from api.models import Entry, get_session
import logging
import json


blueprint = Blueprint('todo', __name__, url_prefix='/todo' )


@blueprint.route('/entry', methods=['GET'])
@login_required
def list_handler():
    session = get_session()
    user = current_user
    logging.debug(user.entries)
    response = make_response(json.dumps(
           [ entry.as_dict() for entry in user.entries ]
       ), 200
    )
    session.close()
    return response

@blueprint.route('/entry', methods=['POST'])
@login_required
def post_handler():
    try:
        body = request.json
        title = body.pop('title')
        completed = body.pop('completed', None)
        description = body.pop('description')
        if body:
            abort(400)

        user = current_user
        entry = Entry(
            title=title,
            completed=completed,
            description=description,
            userid=user.userid
        )
        session = get_session()
        session.add(entry)
        session.commit()
    except (KeyError):
        abort(400)
    response = make_response(json.dumps(
           entry.as_dict()
       ), 201
    )
    session.close()
    return response
