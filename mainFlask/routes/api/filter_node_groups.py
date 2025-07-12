from flask import Blueprint, request, jsonify, abort
from mainFlask.filter_node_object import FilterNodeObject
from mainFlask.filter_node_group import FilterNodeGroup

filter_node_groups_api_bp = Blueprint("filters_api", __name__)

@filter_node_groups_api_bp.get("/api/filter-values")
def filter_node_groups():
    raw_type: str = request.args.get("type", "")

    try:
        ftype = FilterNodeGroup(raw_type)
    except ValueError:
        abort(400, f"Unknown filter type {raw_type!r}")

    values = FilterNodeObject.get_values(ftype) or []
    return jsonify(values)
