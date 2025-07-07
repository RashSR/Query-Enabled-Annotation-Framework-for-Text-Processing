from .api import api_blueprints
from .pages.metrics import metrics_bp
from .pages.settings import settings_bp

blueprints = [*api_blueprints, metrics_bp, settings_bp]
