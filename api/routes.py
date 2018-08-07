from flask import Blueprint, abort, make_response, request
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
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


@blueprint.route('/entry/<int:oid>', methods=['GET'])
@login_required
def get_handler(oid):
    try:
        user = current_user
        session = get_session()
        entry = session.query(Entry).filter(
            Entry.entryid == oid and Entry.userid == user.userid
        ).one()
    except (NoResultFound, MultipleResultsFound):
        abort(404)
    response = make_response(json.dumps(
           entry.as_dict()
       ), 200
    )
    session.close()
    return response


@blueprint.route('/entry/<int:oid>', methods=['DELETE'])
@login_required
def delete_handler(oid):
    try:
        user = current_user
        session = get_session()
        entry = session.query(Entry).filter(
            Entry.entryid == oid and Entry.userid == user.userid
        ).delete()
    except (NoResultFound, MultipleResultsFound):
        abort(404)
    response = make_response(json.dumps(
           entry.as_dict()
       ), 200
    )
    session.close()
    return response


@blueprint.route('/entry/<int:oid>', methods=['PUT'])
@login_required
def put_handler(oid):
    try:
        body = request.json
        title = body.pop('title')
        completed = body.pop('completed', None)
        description = body.pop('description')
        if body:
            abort(400)

        user = current_user
        session = get_session()
        entry = session.query(Entry).filter(
            Entry.entryid == oid and Entry.userid == user.userid
        ).one()

        entry.title = title
        entry.completed = completed if completed is not None else entry.completed
        entry.description = description
        session.add(entry)
        session.commit()
    except (NoResultFound, MultipleResultsFound):
        abort(404)
    response = make_response(json.dumps(
           entry.as_dict()
       ), 200
    )
    session.close()
    return response
