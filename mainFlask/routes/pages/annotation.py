from flask import Blueprint, render_template
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.message import Message
from mainFlask.classes.annotation import Annotation

annotation_bp = Blueprint('annotation', __name__)

@annotation_bp.route("/annotation")
def annotation_view():
    return render_template('annotation.html')

@annotation_bp.route("/annotation/<int:message_id>")
def annotation_view_message(message_id: int):
    #Use_msg ID = 2
    message: Message = CacheStore.Instance().get_message_by_id(message_id)
    print(message)
    for token in message.message_tokens:
        print(token)
    print(message.annotated_text)
    return render_template('annotation.html')
