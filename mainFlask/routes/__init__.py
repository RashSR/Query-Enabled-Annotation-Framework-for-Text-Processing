from .api import api_blueprints
from .pages.metrics import metrics_bp
from .pages.settings import settings_bp
from .pages.chat import chat_bp
from .pages.profile import profile_bp
from .pages.konkordanz import konkordanz_bp
from .pages.annotation import annotation_bp

blueprints = [*api_blueprints, profile_bp, chat_bp, konkordanz_bp, annotation_bp, metrics_bp, settings_bp]
