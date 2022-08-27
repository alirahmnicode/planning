from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "asdnc;jbf;sdfbsa;du"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Plan
    create_database(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import views
    from .auth import auth
    from .planning import plan
    from .habit import habit

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/account')
    app.register_blueprint(plan, url_prefix='/plan/')
    app.register_blueprint(habit, url_prefix='/habit/')

    return app

def create_database(app):
    if not path.exists('website/' + 'db.sqlite'):
        db.create_all(app=app)
        print('created')

