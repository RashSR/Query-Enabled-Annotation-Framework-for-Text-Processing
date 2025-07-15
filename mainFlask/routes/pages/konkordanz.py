from flask import Blueprint, render_template, request
from mainFlask.filter_node_object import FilterNodeObject
from mainFlask.filter_node_group import FilterNodeGroup
from mainFlask.filter_node import FilterNode
from mainFlask.filter_type import FilterType

konkordanz_bp = Blueprint('konkordanz', __name__)

#TODO: the jump dont highlight case sensitiv, keyword gets multiple highlights
#Dem Nutzer die Möglichkeit geben ob er e.g. Fehler in einer Nachricht suchen mag oder direktes Wort oder Nachfolger/Vorgänger
@konkordanz_bp.route("/konkordanz")
def konkordanz_view():

    starting_filter_node  = FilterNode(FilterType.OR)
    tree = parse_query_tree(request.args)
    _convert_tree_to_filter_node(tree, starting_filter_node)

    results = []

    #TODO: bug: if i search for e.g. 'ah' as whole_word AND case_sensitive -> i get two results of the same message and the same hit! 
    if len(starting_filter_node.leaves) > 0:
        results = starting_filter_node.get_full_result() #TODO: check if messages have more search results after and, or and so on

    return render_template(
        "konkordanz.html",
        results=results,
        filter_node_groups=FilterNodeGroup,
        nodes = starting_filter_node.leaves
    )


def parse_query_tree(args):
    # Collect all indices for all relevant fields
    fields = [
        'logic_operator', 'selected_type', 'selected_scope',
        'keyword', 'case_sensitive', 'whole_word', 'use_regex'
    ]
    nodes = {}
    for key, value in args.items():
        for field in fields:
            if key.startswith(f'{field}['):
                idx = key[len(field)+1:-1]  # e.g. '0.1.2'
                nodes.setdefault(idx, {})[field] = value
    # Build tree
    tree = {}
    for idx in sorted(nodes.keys(), key=lambda x: [int(i) for i in x.split('.')]):
        parts = idx.split('.')
        cur = tree
        for p in parts[:-1]:
            cur = cur.setdefault('children', {}).setdefault(p, {})
        cur.setdefault('children', {})[parts[-1]] = nodes[idx]
    return tree.get('children', {})

def _convert_tree_to_filter_node(tree_dict: dict, parent: FilterNode, level: int = 0):
    new_filter_node = None
    selected_type = None #left dropdown
    selected_scope = None

    #only if selected type == 'word'
    keyword = None #searchbar input
    case_sensitive = None
    whole_word = None
    use_regex = None

    for key, value in tree_dict.items():
        print(f"{_make_indents(level)}+Key: {key}, Value: {value}")
        match key:
            case 'logic_operator':
                new_filter_node = FilterNode(FilterType(value)) #muss als parent object übergeben werden
                parent.add_leaf(new_filter_node)
            case 'children':
                print("They are children!")
            case 'selected_type':
                selected_type = value
            case 'selected_scope':
                selected_scope = value
            case 'keyword':
                keyword = value
            case 'case_sensitive':
                case_sensitive = value
            case 'whole_word':
                whole_word = value    
            case 'use_regex':
                use_regex = value
            case _: 
                #default case
                print("default")

        if key == list(tree_dict.keys())[-1]:
            if not selected_type is None:
                new_filter_node_object = FilterNodeObject(FilterNodeGroup(selected_type), keyword, selected_scope, case_sensitive, whole_word, use_regex)
                parent.add_leaf(new_filter_node_object)
                continue

        
        #continue recursion
        if isinstance(value, dict):
            if new_filter_node is None:
                _convert_tree_to_filter_node(value, parent, level+1)
            else:
                _convert_tree_to_filter_node(value, new_filter_node, level+1)

def _make_indents(indents: int) -> str:
    return_string = ""
    for i in range(indents):
        return_string = return_string + "---"

    return return_string