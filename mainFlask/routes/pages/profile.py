from flask import Blueprint, render_template, session, abort, request, jsonify
import utils
from mainFlask.data.cachestore import CacheStore

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