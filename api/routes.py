from flask import Blueprint, abort
from flask_login import current_user


blueprint = Blueprint('todo', __name__)


@blueprint.route('', methods=['GET'])
def list_handler():
    pass
