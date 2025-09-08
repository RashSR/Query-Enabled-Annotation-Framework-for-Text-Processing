import pytest
from mainFlask.classes.annotation import Annotation
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.author import Author
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def establish_db_connection():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    CacheStore.Instance(db, app)

def test_CRUD_annotation(establish_db_connection):
    comment = "Mein Kommentar."
    annotation = Annotation(None, 1, 3, 6, "RULE 43", "Das ist der Grund", comment)
    created_annotation = CacheStore.Instance().create_annotation(annotation)
    assert created_annotation.id is not None
    
    getted_annotation = CacheStore.Instance().get_annotation_by_id(created_annotation.id)
    assert getted_annotation.comment == comment

    getted_annotation.comment = "Das ist der geänderte Kommentar"
    updated_annotation= CacheStore.Instance().update_annotation(getted_annotation)
    assert getted_annotation.comment is not comment

    isDeletionSucessful = CacheStore.Instance().delete_annotation_by_id(updated_annotation.id)
    assert isDeletionSucessful


def test_get_all_annotations_by_msg_id(establish_db_connection):

    #arrange
    msg_id: int = 1 #TODO: create message that this test runs again
    annotation1 = Annotation(None, msg_id, 3, 6, "RULE 43", "Das ist der Grund", "Mein Kommentar.")
    annotation2 = Annotation(None, msg_id, 9, 15, "RULE 5", "Ein anderer Grund", "Mein Kommentar hat sich verändert.")
    annotation3 = Annotation(None, msg_id+2, 9, 15, "RULE 45", "Ein Grund", "Kommentar")
    
    created_annotation1 = CacheStore.Instance().create_annotation(annotation1)
    created_annotation2 = CacheStore.Instance().create_annotation(annotation2)
    created_annotation3 = CacheStore.Instance().create_annotation(annotation3)

    #act
    annotations: list[Annotation] = CacheStore.Instance().get_all_annotations_by_msg_id(msg_id)
    
    #assert
    assert len(annotations) == 2
    assert all(a.message_id == msg_id for a in annotations)
    assert {a.reason for a in annotations} == {"Das ist der Grund", "Ein anderer Grund"}
    assert created_annotation1 in annotations
    assert created_annotation2 in annotations 
    assert created_annotation3 not in annotations

    CacheStore.Instance().delete_annotation_by_id(created_annotation1.id)
    CacheStore.Instance().delete_annotation_by_id(created_annotation2.id)
    CacheStore.Instance().delete_annotation_by_id(created_annotation3.id)

def test_create_author(establish_db_connection):

    #arrange
    author_to_create = Author(None, "Marten", 43, 'Male', 'Deutsch', [], 'Hessen', 'Verkäufer', '')

    #act
    created_author = CacheStore.Instance().create_author(author_to_create)

    #assert
    assert author_to_create is not None
    assert author_to_create.id > 0
    assert author_to_create.name == 'Marten'