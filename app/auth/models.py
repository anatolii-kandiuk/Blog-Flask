from .. import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    about_me = db.Column(db.Text, nullable=False, default='...')
    last_seen = db.Column(db.DateTime, nullable=False, default=db.func.now())
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

db.create_all()