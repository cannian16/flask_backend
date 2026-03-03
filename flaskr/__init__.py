import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ========== 添加健康检查路由（核心）==========
    @app.route('/health')
    def health_check():
        """Cloudflare健康检查端点"""
        return jsonify({"status": "healthy", "service": "cannian-api"}), 200

    @app.route('/')
    def index():
        """根路径返回简单信息，避免404"""
        return jsonify({"message": "API Service is running.", "docs": "Use specific endpoints."}), 200
    # ===========================================

    from . import db
    db.init_app(app)
    # 留言api蓝图
    from . import message
    app.register_blueprint(message.bp)

    from . import friendlink
    app.register_blueprint(friendlink.bp)
    
    return app