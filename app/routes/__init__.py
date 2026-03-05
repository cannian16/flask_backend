from .messages import messages_bp
from .links import links_bp

__all__ = ['messages_bp', 'links_bp']

def register_blueprints(app):
    app.register_blueprint(messages_bp)
    app.register_blueprint(links_bp)