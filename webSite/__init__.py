from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='abhi'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  #telling where the DB is located
    
    db.init_app(app)

    

    from .views import views #we need to register the blueprint fow which we r importing it
    from .auth import auth

    app.register_blueprint(views , url_prefix='/') # registering the view blueprint
    app.register_blueprint(auth , url_prefix='/') # registering the auth blueprint

    from .models import User, Note
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id): # telling flask how you will load a user
        return User.query.get(int(id))

    return app
