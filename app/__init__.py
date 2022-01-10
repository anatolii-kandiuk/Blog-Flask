from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_admin import Admin
from config import config


class App:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
            cls.instance.__app = Flask(__name__)
            cls.instance.__app.config.from_object('config')
        return cls.instance

    def get_app(self):
        return self.__app


app = App().get_app()
bcrypt = Bcrypt()
db = SQLAlchemy()
admin = Admin()
migrate = Migrate()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    """Construct the core application."""
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    admin.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from app import views

        from .auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

        # from .form import form_blueprint
        # app.register_blueprint(form_blueprint, url_prefix='/form')

        from .posts import posts
        app.register_blueprint(posts, url_prefix='/post')

        from .personal_computers import personal_computers
        app.register_blueprint(personal_computers, url_prefix='/personal_computers')

        from .api import api
        app.register_blueprint(api, url_prefix='/api')

        return app

