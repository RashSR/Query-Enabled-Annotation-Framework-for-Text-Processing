from .api import api_blueprints
from .pages.metrics import metrics_bp
from .pages.settings import settings_bp
from .pages.chat import chat_bp

blueprints = [*api_blueprints, chat_bp, metrics_bp, settings_bp]
