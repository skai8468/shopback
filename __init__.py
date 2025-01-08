from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "mydb"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    # Replace this line with your MySQL connection URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/mydb'
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .model import User, Purchase, Store
    with app.app_context():
        db.create_all()
    
    return app
