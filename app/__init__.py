from flask import Flask
from .extensions import db
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()  # 加载 .env 文件中的环境变量到内存里，别的模块不需要再加载一次了
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # 打印 SQL 语句（调试用）
    app.secret_key = os.getenv('SECRET_KEY')

    CORS(app,
         origins=["http://localhost:4321"],
         supports_credentials=True) # 允许所有来源的跨域请求

    db.init_app(app)

    from . import models
    
    with app.app_context():
        # Create database tables
        db.create_all()

    @app.route('/')
    def hello():
        return 'Hello, World!'

    from .routes import register_blueprints
    register_blueprints(app)
    
    return app