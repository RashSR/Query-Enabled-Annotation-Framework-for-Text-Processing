from flask import Blueprint, render_template
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.message import Message
from mainFlask.classes.annotation import Annotation

annotation_bp = Blueprint('annotation', __name__)

@annotation_bp.route("/annotation")
def annotation_view():
    annotation = Annotation(None, 1, 3, 6, "RULE 43", "Das ist der Grund", "Mein Kommentar.")
    print(annotation)
    
    created_annotation = CacheStore.Instance().create_annotation(annotation)
    print(created_annotation)
    
    getted_annotation = CacheStore.Instance().get_annotation_by_id(1)
    print(getted_annotation)

    getted_annotation.comment = "Das ist der geänderte Kommentar"
    updated_annotation= CacheStore.Instance().update_annotation(getted_annotation)
    print(updated_annotation)

    if(CacheStore.Instance().delete_annotation_by_id(updated_annotation.id)):
        print("Erfolgreich gelöscht!")

    return render_template('annotation.html')

@annotation_bp.route("/annotation/<int:message_id>")
def annotation_view_message(message_id: int):
    message: Message = CacheStore.Instance().get_message_by_id(message_id)
    print(message)
    return render_template('annotation.html')
