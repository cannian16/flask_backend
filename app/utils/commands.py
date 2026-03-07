import click
from flask.cli import with_appcontext
from app.extensions import db 
from app.models import *

def register_commands(app):
    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """清除数据并重新初始化数据库表结构 (慎用)"""
        # 如果你想保留数据，只加新表，去掉下面这一行
        # db.drop_all() 
        
        db.create_all()
        click.echo("数据库已成功初始化！")