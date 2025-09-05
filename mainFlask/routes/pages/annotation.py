from flask import Blueprint, render_template, request, jsonify
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
    #for token in message.message_tokens:
        #print(token)
    print(message.annotated_text)
    return render_template('annotation.html', message=message)

def save_annotation_comment(annotation_id: int, new_comment: str):
    annotation_to_update = CacheStore.Instance().get_annotation_by_id(annotation_id)
    annotation_to_update.comment = new_comment
    isUpdated = CacheStore.Instance().update_annotation(annotation_to_update)
    return isUpdated

@annotation_bp.route('/save_annotation_comment', methods=['POST'])
def save_annotation_comment_route():
    annotation_id = request.form.get('annotation_id', type=int)
    new_comment = request.form.get('new_comment', type=str)
    # Call your method (should return True/False)
    success = save_annotation_comment(annotation_id, new_comment)
    return jsonify({'success': bool(success)})
