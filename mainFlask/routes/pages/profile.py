from flask import Blueprint, render_template, session, abort, request, jsonify
import utils
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.author import Author
from mainFlask.classes.message import Message
from mainFlask.classes.chat import Chat

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile")
def profile():
    all_authors = CacheStore.Instance().get_all_authors()
    return render_template("profile.html", author=utils.get_active_author(session), authors=all_authors)

@profile_bp.route("/profile/<int:author_id>")
def author_profile(author_id):
    all_authors = CacheStore.Instance().get_all_authors()
    selected_author = CacheStore.Instance().get_author_by_id(author_id)
    if not selected_author:
        abort(404)
    if not request.args.get('no_active_change'):
        utils.set_active_author(session, author_id)
        selected_author = utils.get_active_author(session)
    return render_template("profile.html", author=selected_author, authors=all_authors)

@profile_bp.route("/profile/<int:author_id>/annotation", methods=["POST"])
def save_author_annotation(author_id):
    data = request.get_json()
    annotation = data.get('annotation', '')
    author = CacheStore.Instance().get_author_by_id(author_id)
    if not author:
        return jsonify({'error': 'Not found'}), 404
    author.annotation = annotation
    author = CacheStore.Instance().update_author(author, column_name="annotation", value=annotation)
    return jsonify({'success': True})

@profile_bp.route('/add_author', methods=['POST'])
def add_author():
    data = request.get_json()
    name = data.get('name', '')
    age = data.get('age', '')
    gender = data.get('gender', '')
    first_language = data.get('first_language', '')
    languages = data.get('languages', '')
    region = data.get('region', '')
    job = data.get('job', '')
    author_to_create = Author(None, name, age, gender, first_language, languages, region, job)
    created_author = CacheStore.Instance().create_author(author_to_create)
    success = created_author is not None
    author_id = created_author.id if success else None
    return jsonify({'success': success, 'author_id': author_id})

@profile_bp.route('/delete_author', methods=['POST'])
def delete_author():
    data = request.get_json()
    author_id = data.get('author_id', None)
    if not author_id:
        return jsonify({'success': False})
    deleted = CacheStore.Instance().delete_author_by_id(author_id)
    if deleted:
        utils.set_active_author(session, None)
    return jsonify({'success': bool(deleted)})

@profile_bp.route('/profile/<int:author_id>/add_chat', methods=['POST'])
def add_chat(author_id):
    chat_file = request.files.get('chat_file')

    if not chat_file or not chat_file.filename.endswith('.txt'):
        return jsonify({'success': False, 'error': 'Invalid file'}), 400
    
    try:
        file_content = chat_file.read().decode('utf-8')
        msg_list: list[Message] = utils.get_messages_from_text(file_content)
        distinct_senders = {msg.sender for msg in msg_list}
        distinct_senders_list = list(distinct_senders)
        # Prepare extracted authors for frontend (as names)
        extracted_authors = [str(sender) for sender in distinct_senders_list]
        # Get all existing authors (id and name)
        all_authors = CacheStore.Instance().get_all_authors()
        existing_authors = [{'id': a.id, 'name': a.name} for a in all_authors]
        return jsonify({
            'success': True,
            'extracted_authors': extracted_authors,
            'existing_authors': existing_authors
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@profile_bp.route('/profile/<int:author_id>/map_chat_authors', methods=['POST'])
def map_chat_authors(author_id):
    data = request.get_json()
    mapped_author_ids = data.get('mapping', []) # List of selected author IDs from modal
    extracted_authors = data.get('extracted_authors', [])  # Names of extracted authors
    relationship = data.get('relationship', '')  # Relationship between authors

    mapped_info = [
        {'extracted': extracted, 'mapped_id': mapped_id}
        for extracted, mapped_id in zip(extracted_authors, mapped_author_ids)
    ]

    author1_id = int(mapped_info[0]["mapped_id"])
    author2_id = int(mapped_info[1]["mapped_id"])
    author_1 = CacheStore.Instance().get_author_by_id(author1_id)
    author_2 = CacheStore.Instance().get_author_by_id(author2_id)

    chat_to_create: Chat = Chat(None)
    chat_to_create.participants.append(author_1)
    chat_to_create.participants.append(author_2)
    chat_to_create.relation = relationship
    print(relationship)
    created_chat = CacheStore.Instance().create_chat(chat_to_create)
    
    print(f"Received author mapping for chat upload: {mapped_info}")
    print(f"Relationship between authors: {relationship}")
    return jsonify({'success': True, 'mapped_info': mapped_info, 'relationship': relationship})

