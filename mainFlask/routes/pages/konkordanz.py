from flask import Blueprint, render_template, request
from mainFlask.classes.filter_node_object import FilterNodeObject
from mainFlask.classes.filter_node_group import FilterNodeGroup
from mainFlask.classes.filter_node import FilterNode
from mainFlask.classes.filter_type import FilterType

konkordanz_bp = Blueprint('konkordanz', __name__)

#TODO: the jump dont highlight case sensitiv, keyword gets multiple highlights
#Dem Nutzer die Möglichkeit geben ob er e.g. Fehler in einer Nachricht suchen mag oder direktes Wort oder Nachfolger/Vorgänger
@konkordanz_bp.route("/konkordanz")
def konkordanz_view():

    #create a filter node that is not visible to the user -> all nodes are under this
    starting_filter_node  = FilterNode(FilterType.OR)
    tree = parse_query_tree(request.args)
    _convert_tree_to_filter_node(tree, starting_filter_node)

    results = []

    if len(starting_filter_node.leaves) > 0:
        results = starting_filter_node.get_full_result()

    def serialize_node(node):
        # FilterNodeObject (leaf)
        if hasattr(node, 'filter_node_group'):
            return {
                'filter_node_group': node.filter_node_group,
                'searchbar_input': getattr(node, 'searchbar_input', None),
                'selected_value': getattr(node, 'selected_value', None),
                'scope_choices': getattr(node, 'scope_choices', []),
                'case_sensitive': getattr(node, 'case_sensitive', False),
                'whole_word': getattr(node, 'whole_word', False),
                'use_regex': getattr(node, 'use_regex', False),
                'search_result_list': getattr(node, 'search_result_list', []),
                'search_results': getattr(node, 'search_result_list', []),
                'children': None
            }
        # FilterNode (logic node)
        elif hasattr(node, 'leaves'):
            return {
                'filter_type': getattr(node, 'filter_type', None),
                'token_range': getattr(node, 'token_range', None),
                'children': [serialize_node(child) for child in node.leaves],
                'search_results': getattr(node, 'search_results', []),
            }
        return {}

    # Only pass top-level nodes (children of invisible root), but keep their structure
    nodes = [serialize_node(child) for child in getattr(starting_filter_node, 'leaves', [])]

    return render_template(
        "konkordanz.html",
        results=results,
        filter_node_groups=FilterNodeGroup,
        nodes=nodes
    )

def parse_query_tree(args):
    # Collect all indices for all relevant fields
    fields = [
        'logic_operator', 'selected_type', 'selected_scope',
        'keyword', 'case_sensitive', 'whole_word', 'use_regex', 'token_range'
    ]
    nodes = {}
    for key, value in args.items():
        for field in fields:
            if key.startswith(f'{field}['):
                idx = key[len(field)+1:-1]  #e.g. '0.1.2'
                nodes.setdefault(idx, {})[field] = value

    tree = {}
    for idx in sorted(nodes.keys(), key=lambda x: [int(i) for i in x.split('.')]):
        parts = idx.split('.')
        cur = tree
        for p in parts[:-1]:
            cur = cur.setdefault('children', {}).setdefault(p, {})
        cur.setdefault('children', {})[parts[-1]] = nodes[idx]
    return tree.get('children', {})

def _convert_tree_to_filter_node(tree_dict: dict, parent: FilterNode):
    new_filter_node = None
    leaf_data = {'selected_type': None, 'selected_scope': None, 'keyword': None,
        'case_sensitive': None, 'whole_word': None, 'use_regex': None }
    token_range_value = None

    for i, (key, value) in enumerate(tree_dict.items()):
        match key:
            case 'logic_operator':
                new_filter_node = FilterNode(FilterType(value))
                parent.add_leaf(new_filter_node)
            case 'token_range':
                try:
                    token_range_value = int(value)
                except Exception:
                    token_range_value = 0
            case 'selected_type' | 'selected_scope' | 'keyword' | 'case_sensitive' | 'whole_word' | 'use_regex':
                leaf_data[key] = value

        #if last index is reached and left dropdown is selected -> create new fno 
        if i == len(tree_dict) - 1 and leaf_data['selected_type']:
            node_object = FilterNodeObject(
                FilterNodeGroup(leaf_data['selected_type']),
                leaf_data['keyword'],
                leaf_data['selected_scope'],
                leaf_data['case_sensitive'],
                leaf_data['whole_word'],
                leaf_data['use_regex']
            )
            parent.add_leaf(node_object)
        
        #continue recursion
        if isinstance(value, dict):
            child_parent = new_filter_node if new_filter_node else parent
            # If this is an AND node and token_range_value is set, assign it
            if new_filter_node and hasattr(new_filter_node, 'filter_type') and new_filter_node.filter_type == FilterType.AND and token_range_value is not None:
                new_filter_node.token_range = token_range_value
            _convert_tree_to_filter_node(value, child_parent)
