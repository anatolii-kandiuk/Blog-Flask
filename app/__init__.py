from flask_sqlalchemy import SQLAlchemy
from .app import App
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = App().get_app()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

from . import views
from .auth import auth
from .personal_computers import personal_computers
#from .forms import form

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(personal_computers, url_prefix='/personal_computers')
#app.register_blueprint(form, url_prefix='/forms')