from flask import Blueprint, request, jsonify

from controllers.notes_controller import create_note, get_note, share_note, update_note, get_note_version_history
from middlewares.auth_middleware import verify_token

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/create', methods=['POST'])
@verify_token
def create_note_route():
    request_data = request.get_json()
    title = request_data.get('title')
    content = request_data.get('content')
    author_id = request.user['id']
    
    create_note_response, status_code = create_note(title, content, author_id)
    return jsonify(create_note_response), status_code


@notes_bp.route('/<int:note_id>', methods=['GET'])
@verify_token
def get_note_route(note_id):
    author_id = request.user['id']
    get_note_response, status_code = get_note(note_id, author_id)
    
    return jsonify(get_note_response), status_code


@notes_bp.route('/share', methods=['POST'])
@verify_token
def share_note_route():
    request_data = request.get_json()
    note_id = request_data.get('note_id')
    usernames = request_data.get('usernames', [])
    
    share_note_response, status_code = share_note(note_id, usernames)
    return jsonify(share_note_response), status_code


@notes_bp.route('/<int:note_id>', methods=['PUT'])
@verify_token
def update_note_route(note_id):
    request_data = request.get_json()
    author_id = request.user['id']
    
    update_note_response, status_code = update_note(note_id, author_id, **request_data)
    return jsonify(update_note_response), status_code
    
    
@notes_bp.route('/version-history/<int:note_id>', methods=['GET'])
@verify_token
def get_note_version_history_route(note_id):
    author_id = request.user['id']
    
    get_note_version_history_response, status_code = get_note_version_history(note_id, author_id)
    return jsonify(get_note_version_history_response), status_code
    