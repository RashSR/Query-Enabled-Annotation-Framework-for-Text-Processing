from flask import Blueprint, render_template, request
from mainFlask.data.cachestore import CacheStore

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route("/metrics")
def metrics_view():
    authors = CacheStore.Instance().get_all_authors()
    return render_template('metrics.html', authors=authors)


@metrics_bp.route("/metrics/<int:author_id>")
def metrics_author(author_id):
    authors = CacheStore.Instance().get_all_authors()
    # You can add more logic here to show metrics for the selected author
    return render_template('metrics.html', authors=authors, selected_author_id=author_id)
