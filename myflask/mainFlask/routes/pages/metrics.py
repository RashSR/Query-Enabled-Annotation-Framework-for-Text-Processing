from flask import Blueprint, render_template

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route("/metrics")
def metrics_view():
    return render_template('metrics.html')
