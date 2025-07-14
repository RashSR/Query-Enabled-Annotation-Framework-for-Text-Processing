from flask import Blueprint, render_template, session, request
from mainFlask.filter_node_object import FilterNodeObject
from mainFlask.filter_node_group import FilterNodeGroup
from mainFlask.filter_node import FilterNode
from mainFlask.filter_type import FilterType
from mainFlask.settings import Settings

konkordanz_bp = Blueprint('konkordanz', __name__)

#TODO: the jump dont highlight case sensitiv, keyword gets multiple highlights
#Dem Nutzer die Möglichkeit geben ob er e.g. Fehler in einer Nachricht suchen mag oder direktes Wort oder Nachfolger/Vorgänger
@konkordanz_bp.route("/konkordanz")
def konkordanz_view():

    settings = Settings.Instance()

    # Print all hierarchical query params for debugging
    print('--- Hierarchical Query Params ---')
    for k, v in request.args.items():
        print(f'{k}: {v}')

    print('-------------------------------')
    filter_node_object_count = len([k for k in request.args if k.startswith('selected_type[')])
    starting_filter_node  = FilterNode(FilterType.AND)

    results = []

    for i in range(filter_node_object_count):
        searchbar_input   = request.args.get(f'keyword[{i}]', '')
        selected_type  = request.args.get(f'selected_type[{i}]')
        selected_scope  = request.args.get(f'selected_scope[{i}]')
        case_sensitive = bool(request.args.get(f'case_sensitive[{i}]'))
        whole_word = bool(request.args.get(f'whole_word[{i}]'))
        use_regex = bool(request.args.get(f'use_regex[{i}]'))
        fno = FilterNodeObject(FilterNodeGroup(selected_type), searchbar_input, selected_scope, case_sensitive, whole_word, use_regex)
        fno.selected_color = settings.highlight_colors[i % len(settings.highlight_colors)]
        fno.scope_choices = FilterNodeObject.get_values(fno.filter_node_group)
        starting_filter_node.add_leaf(fno)

    if filter_node_object_count > 0:
        results = starting_filter_node.get_full_result() #TODO: check if messages have more search results after and, or and so on

    return render_template(
        "konkordanz.html",
        results=results,
        filter_node_groups=FilterNodeGroup,
        nodes = starting_filter_node.leaves
    )