#this file makes the website folder a python package
#this means that we can import the website folder and use it anywhere
#whenever we import the website folder, whatever is inside the __init__.py file will run automatically

##SETTING UP OUR FLASK FILE

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'i am shsohshog' #primarily used to sign cookies, enusuring that cookies are secure and cannot be tampered with
    #When Flask creates a session for a user, it serializes the data into a cookie on the client side. 
    #The SECRET_KEY is used to sign this cookie cryptographically, preventing malicious actors from modifying it.

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    

    from .views import views #importing the views blueprint
    from .auth import auth  #importing the auth blueprint

    app.register_blueprint(views, url_prefix='/') #registering the blueprint
    app.register_blueprint(auth, url_prefix='/') #registering the blueprint

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #the flask file will redirect to the login page when not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id): #we pass an id
        return User.query.get(int(id)) #it checks for the id and loads the user

    return app

def create_database(app):
    if not path.exists('/website/' + DB_NAME): #if the database does not exist already, then its created
        with app.app_context():
            db.create_all()
            print("Data Created!")
