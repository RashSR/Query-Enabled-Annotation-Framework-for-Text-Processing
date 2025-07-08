from flask import Blueprint, request, jsonify, abort, session
from mainFlask.filter_node_object import FilterNodeObejct
from mainFlask.filter_node_group import FilterNodeGroup
import utils

filter_node_groups_api_bp = Blueprint("filters_api", __name__)

@filter_node_groups_api_bp.get("/api/filter-values")
def filter_node_groups():
    raw_type = request.args.get("type", "")

    try:
        ftype = FilterNodeGroup(raw_type)
    except ValueError:
        abort(400, f"Unknown filter type {raw_type!r}")

    author = utils.get_active_author(session)
    author.analyze_all_own_messages()  # TODO: should be unnecessary

    values = FilterNodeObejct.get_values(ftype, author) or []
    return jsonify(values)
