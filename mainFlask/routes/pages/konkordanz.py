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

    starting_filter_node  = FilterNode(FilterType.AND)
    tree = parse_query_tree(request.args)
    _convert_tree_to_filter_node(tree)
    # Print all hierarchical query params for debugging
    
    #print('--- Hierarchical Query Params ---')
    #for k, v in request.args.items():
        #print(f'{k}: {v}')

    #sfilter_node_object_count = len([k for k in request.args if k.startswith('selected_type[')])

    results = []
    if False:
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


def parse_query_tree(args):
    """
    Parses hierarchical query params (e.g. selected_type[0.1.2]) into a nested tree structure.
    Returns a nested dict representing the tree.
    """
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

def _convert_tree_to_filter_node(tree_dict: dict, level: int = 0):
    for key, value in tree_dict.items():
        print(f"{_make_indents(level)}+Key: {key}, Value: {value}")
        if key == 'logic_operator':
            new_filter_node = FilterNode(FilterType(value))
            print(new_filter_node)
            #auf ebene von von hier hat man immer noch 

        if isinstance(value, dict):
            _convert_tree_to_filter_node(value, level+1)

def _make_indents(indents: int) -> str:
    return_string = ""
    for i in range(indents):
        return_string = return_string + "---"

    return return_string


#       public static void printMyTree(Node root) {
#           if (root.getRoot() == null) {
#               root.printNode();
#           }
#
#           if (root.getLeafCount() > 0 && root != null) {
#               Iterator var1 = root.getLeafs().iterator();
#
#               while(var1.hasNext()) {
#                    Node leaf = (Node)var1.next();
#                   leaf.printNode();
#                   printMyTree(leaf);
#               }
#           }
#       }
#