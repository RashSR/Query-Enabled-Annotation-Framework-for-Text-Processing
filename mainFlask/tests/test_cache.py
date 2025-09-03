from mainFlask.classes.annotation import Annotation
from mainFlask.data.cachestore import CacheStore

def test_CRUD_annotation():
    annotation = Annotation(None, 1, 3, 6, "RULE 43", "Das ist der Grund", "Mein Kommentar.")
    print(annotation)
    
    created_annotation = CacheStore.Instance().create_annotation(annotation)
    print(created_annotation)
    
    getted_annotation = CacheStore.Instance().get_annotation_by_id(created_annotation.id)
    print(getted_annotation)

    getted_annotation.comment = "Das ist der geänderte Kommentar"
    updated_annotation= CacheStore.Instance().update_annotation(getted_annotation)
    print(updated_annotation)

    if(CacheStore.Instance().delete_annotation_by_id(updated_annotation.id)):
        print("Erfolgreich gelöscht!")

def test_get_all_annotations_by_msg_id():
    msg_id: int = 1
    annotation1 = Annotation(None, msg_id, 3, 6, "RULE 43", "Das ist der Grund", "Mein Kommentar.")
    created_annotation1 = CacheStore.Instance().create_annotation(annotation1)
    annotation2 = Annotation(None, msg_id, 9, 15, "RULE 5", "Ein anderer Grund", "Mein Kommentar hat sich verändert.")
    created_annotation2 = CacheStore.Instance().create_annotation(annotation2)
    annotation3 = Annotation(None, msg_id+2, 9, 15, "RULE 45", "Ein Grund", "Kommentar")
    created_annotation3 = CacheStore.Instance().create_annotation(annotation3)
    annotations: list[Annotation] = CacheStore.Instance().get_all_annotations_by_msg_id(msg_id)
    if len(annotations) == 2:
        print("true")
    for annotation in annotations:
        print(annotation)