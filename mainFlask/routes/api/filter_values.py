from flask import Blueprint, request, jsonify, abort, session
from mainFlask.filter_node_object import FilterNodeObejct
from mainFlask.filter_type import FilterType
import utils

filter_values_api_bp = Blueprint("filters_api", __name__)

@filter_values_api_bp.get("/api/filter-values")
def filter_values():
    raw_type = request.args.get("type", "")

    try:
        ftype = FilterType(raw_type)
    except ValueError:
        abort(400, f"Unknown filter type {raw_type!r}")

    author = utils.get_active_author(session)
    author.analyze_all_own_messages()  # TODO: should be unnecessary

    values = FilterNodeObejct.get_values(ftype, author) or []
    return jsonify(values)
