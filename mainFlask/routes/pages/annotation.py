from flask import Blueprint, render_template

annotation_bp = Blueprint('annotation', __name__)

@annotation_bp.route("/annotation")
def annotation_view():
    return render_template('annotation.html')
