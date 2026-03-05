from .messages import messages_bp

__all__ = ['messages_bp']

def register_blueprints(app):
    app.register_blueprint(messages_bp)