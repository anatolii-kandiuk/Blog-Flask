from .. import db

import enum

class PostType(enum.Enum):
    Flask = 'Flask'
    Django = 'Django'
    Other = 'Other'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='post_default.jpg')
    created = db.Column(db.Date, nullable=False, default=db.func.now())
    type = db.Column(db.Enum(PostType))
    enabled = db.Column(db.Boolean, nullable=False, default=True,)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.text}', '{self.created}')"

#db.create_all()