from flask import Blueprint, render_template, session, abort, request, jsonify
import utils
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.author import Author
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

# AJAX endpoint to save annotation
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
    return jsonify({'success': bool(deleted)})

@profile_bp.route('/profile/<int:author_id>/add_chat', methods=['POST'])
def add_chat(author_id):
    chat_file = request.files.get('chat_file')
    file_content = chat_file.read().decode('utf-8')
    utils.load_single_chat_from_file(file_content)
    if not chat_file or not chat_file.filename.endswith('.txt'):
        return jsonify({'success': False, 'error': 'Invalid file'}), 400
    try:
        file_content = chat_file.read().decode('utf-8')
        if not utils.validate_chat_format(file_content):
            print("i am here")
            return jsonify({'success': False, 'error': str(e)}), 500
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

