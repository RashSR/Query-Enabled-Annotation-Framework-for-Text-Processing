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


def save_annotation_comment(annotation_id: int, new_comment: str, grund: str, annotation_text: str, start_pos: int, end_pos: int):
    annotation_to_update = CacheStore.Instance().get_annotation_by_id(annotation_id)
    print(f"{new_comment},{grund},{annotation_text},{start_pos},{end_pos}")
    annotation_to_update.comment = new_comment
    annotation_to_update.reason = grund
    annotation_to_update.annotation = annotation_text
    annotation_to_update.start_pos = start_pos
    annotation_to_update.end_pos = end_pos
    isUpdated = CacheStore.Instance().update_annotation(annotation_to_update)
    return isUpdated

@annotation_bp.route('/save_annotation_comment', methods=['POST'])

def save_annotation_comment_route():
    annotation_id = request.form.get('annotation_id', type=int)
    new_comment = request.form.get('new_comment', type=str)
    grund = request.form.get('grund', type=str)
    annotation_text = request.form.get('annotation', type=str)
    start_pos = request.form.get('start_pos', type=int)
    end_pos = request.form.get('end_pos', type=int)
    success = save_annotation_comment(annotation_id, new_comment, grund, annotation_text, start_pos, end_pos)
    return jsonify({'success': bool(success)})
