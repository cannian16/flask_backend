from flask import Flask
from .extensions import db
from flask_cors import CORS
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # 打印 SQL 语句（调试用）
    app.secret_key = 'dev'

    CORS(app,
         origins=["http://localhost:4321"],
         supports_credentials=True) # 允许所有来源的跨域请求

    db.init_app(app)

    from . import models
    
    with app.app_context():
        # Create database tables
        db.create_all()

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    from .routes import register_blueprints
    register_blueprints(app)
    
    return app