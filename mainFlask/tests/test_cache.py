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