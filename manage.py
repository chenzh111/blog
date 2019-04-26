from flask import Flask
from flask_script import Manager
from back.model import db
from back.view import back
from web.view import web

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456aadadadadasda'
app.config['PERMANENT_SESSION_LIFETIME'] = 10
app.register_blueprint(blueprint=back, url_prefix='/back/')
app.register_blueprint(blueprint=web, url_prefix='/web/')

# 配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@39.97.107.197:3306/flask1'
db.init_app(app)

manage = Manager(app)

if __name__ == "__main__":
    manage.run()
