from flask import Blueprint, render_template, request, abort
from mainFlask.data.cachestore import CacheStore

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route("/metrics")
def metrics_view():
    all_authors = CacheStore.Instance().get_all_authors()
    return render_template('metrics.html', authors=all_authors)


@metrics_bp.route("/metrics/<int:author_id>")
def metrics_author(author_id):
    all_authors = CacheStore.Instance().get_all_authors()
    selected_author = CacheStore.Instance().get_author_by_id(author_id)
    if not selected_author:
        abort(404)
    return render_template('metrics.html', authors=all_authors, author=selected_author)
