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
    message: Message = CacheStore.Instance().get_message_by_id(message_id)
    return render_template('annotation.html', message=message)

@annotation_bp.route('/save_annotation', methods=['POST'])
def save_annotation():
    position = request.form.get('position')
    annotation = request.form.get('annotation')
    grund = request.form.get('grund')
    kommentar = request.form.get('kommentar')
    message_id = int(request.form.get('message_id'))
    start_pos, end_pos = map(int, position.split("-"))

    annotation_to_create = Annotation(None, message_id, start_pos, end_pos, annotation, grund, kommentar)
    created_annotation = CacheStore.Instance().create_annotation(annotation_to_create)
    IsCreationSucessfully = created_annotation is not None

    return jsonify({'success': bool(IsCreationSucessfully)})

@annotation_bp.route('/update_annotation', methods=['POST'])

def save_annotatio_route():
    annotation_id = request.form.get('annotation_id', type=int)
    new_comment = request.form.get('new_comment', type=str)
    grund = request.form.get('grund', type=str)
    annotation_text = request.form.get('annotation', type=str)
    start_pos = request.form.get('start_pos', type=int)
    end_pos = request.form.get('end_pos', type=int)
    success = update_annotation(annotation_id, new_comment, grund, annotation_text, start_pos, end_pos)
    return jsonify({'success': bool(success)})

def update_annotation(annotation_id: int, new_comment: str, grund: str, annotation_text: str, start_pos: int, end_pos: int):
    annotation_to_update = CacheStore.Instance().get_annotation_by_id(annotation_id)
    annotation_to_update.comment = new_comment
    annotation_to_update.reason = grund
    annotation_to_update.annotation = annotation_text
    annotation_to_update.start_pos = start_pos
    annotation_to_update.end_pos = end_pos
    isUpdated = CacheStore.Instance().update_annotation(annotation_to_update)
    return isUpdated

@annotation_bp.route('/delete_annotation', methods=['POST'])
def delete_annotation_route():
    annotation_id = request.form.get('annotation_id', type=int)
    success = CacheStore.Instance().delete_annotation_by_id(annotation_id)
    return jsonify({'success': bool(success)})

@annotation_bp.route('/delete_spacy_match', methods=['POST'])
def delete_spacy_match():
    spacy_match_id = request.form.get('id', type=int)
    success = CacheStore.Instance().delete_spacy_match_by_id(spacy_match_id)
    return jsonify({'success': bool(success)})

@annotation_bp.route('/delete_error', methods=['POST'])
def delete_error():
    lt_match_id = request.form.get('id', type=int)
    success = CacheStore.Instance().delete_lt_match_by_id(lt_match_id)
    return jsonify({'success': bool(success)})

# Update a Fehlerliste (error list) entry (e.g., category)
@annotation_bp.route('/update_error', methods=['POST'])
def update_error_route():
    error_id = request.form.get('id', type=int)
    new_category = request.form.get('category', type=str)
    start_pos = request.form.get('start_pos', type=int)
    end_pos = request.form.get('end_pos', type=int)
    rule_id = request.form.get('rule_id', type=str)
    print(f"values: {error_id},{new_category},{start_pos},{end_pos},{rule_id}")
    success = True#update_error(error_id, new_category, start_pos, end_pos, rule_id)
    return jsonify({'success': bool(success)})

def update_error(error_id: int, new_category: str, start_pos: int, end_pos: int, rule_id: str):
    error_to_update = CacheStore.Instance().get_lt_match_by_id(error_id)
    if not error_to_update:
        return False
    error_to_update.category = new_category
    error_to_update.start_pos = start_pos
    error_to_update.end_pos = end_pos
    error_to_update.rule_id = rule_id
    isUpdated = CacheStore.Instance().update_lt_match(error_to_update)
    return isUpdated



