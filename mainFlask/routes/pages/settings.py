from flask import Blueprint, render_template
settings_bp = Blueprint('settings', __name__)

@settings_bp.route("/settings")
def settings_view():
    return render_template("settings.html")
