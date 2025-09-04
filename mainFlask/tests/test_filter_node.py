import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.filter_node import FilterNode
from mainFlask.classes.filter_node_object import FilterNodeObject
from mainFlask.classes.filter_node_group import FilterNodeGroup
from mainFlask.classes.filter_type import FilterType

@pytest.fixture
def establish_db_connection():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'  #TODO: this needs own db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    CacheStore.Instance(db, app)

def test_filter_node(establish_db_connection):
    #build starting node with two FNOs
    starting_test_node = FilterNode(FilterType.OR)
    categoryNode = FilterNodeObject(FilterNodeGroup("error-category"), None, "CASING")
    authorNode = FilterNodeObject(FilterNodeGroup('author'), None, 'Ben Vector')
    starting_test_node.add_leaf(categoryNode)
    starting_test_node.add_leaf(authorNode)

    #build sub node with 1 FNO
    sub_and_node = FilterNode(FilterType.AND)
    rule_id_node = FilterNodeObject(FilterNodeGroup("error-ruleId"), None, 'PFEILE')
    sub_and_node.add_leaf(rule_id_node)

    #add sub node to root note
    starting_test_node.add_leaf(sub_and_node)

    #confirm with print
    starting_test_node.print_leave_structure()

    #to get this structure:
    #+Type: FilterType.AND, Leaves: 3
    #---+filter_node_group: FilterNodeGroup.CATEGORY, input: None, selected_value: CASING
    #---+filter_node_group: FilterNodeGroup.AUTHOR, input: None, selected_value: Ben Vector
    #---+Type: FilterType.AND, Leaves: 1
    #------+filter_node_group: FilterNodeGroup.RULE_ID, input: None, selected_value: PFEILE

    #getting result
    test_result = starting_test_node.get_full_result()
    print(len(test_result))