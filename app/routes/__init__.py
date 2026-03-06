from .messages import messages_bp
from .links import links_bp
from .songs import songs_bp
from .skills import skills_bp
from .tools import tools_bp

__all__ = ['messages_bp', 'links_bp', 'songs_bp', 'skills_bp', 'tools_bp']

def register_blueprints(app):
    app.register_blueprint(messages_bp)
    app.register_blueprint(links_bp)
    app.register_blueprint(songs_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(tools_bp)