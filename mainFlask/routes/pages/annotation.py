from flask import Blueprint, render_template
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.message import Message

annotation_bp = Blueprint('annotation', __name__)

@annotation_bp.route("/annotation")
def annotation_view():

    messages: list[Message] = CacheStore.Instance().get_all_messages()
    for msg in messages:
        x = msg.message_tokens
        if(msg.message_id == 1):
            for token in msg.message_tokens:
                print(token)
    return render_template('annotation.html')

@annotation_bp.route("/annotation/<int:message_id>")
def annotation_view_message(message_id: int):
    message: Message = CacheStore.Instance().get_message_by_id(message_id)
    return render_template('annotation.html')
