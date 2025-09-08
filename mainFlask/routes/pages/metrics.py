from flask import Blueprint, render_template
from mainFlask.data.cachestore import CacheStore

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route("/metrics")
def metrics_view():
    authors = CacheStore.Instance().get_all_authors()
    return render_template('metrics.html', authors=authors)
