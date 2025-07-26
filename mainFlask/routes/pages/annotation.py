from flask import Blueprint, render_template
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.message import Message

annotation_bp = Blueprint('annotation', __name__)

@annotation_bp.route("/annotation")
def annotation_view():

    messages: list[Message] = CacheStore.Instance().get_all_messages()
    for msg in messages:
        x = msg.message_tokens
    return render_template('annotation.html')
