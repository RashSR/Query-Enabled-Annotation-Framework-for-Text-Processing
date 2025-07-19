from flask import Blueprint, render_template
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.message import Message
import utils
settings_bp = Blueprint('settings', __name__)

@settings_bp.route("/settings")
def settings_view():

    all_messages = CacheStore.Instance().get_all_messages()
    all_msgs_as_one = ""
    for msg in all_messages:
        all_msgs_as_one = all_msgs_as_one + msg.content
    big_message = Message(7, 23434, CacheStore.Instance().get_author_by_id(1), None, all_msgs_as_one)
    tags = list(set(utils.analyze_msg_with_spacy(big_message)))
    print(tags)

    return render_template("settings.html")
