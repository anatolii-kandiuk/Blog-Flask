from .. import db

import enum

# post_tag = db.Table(
#     db.Column('id', db.Integer, db.ForeignKey('post_tag.id')),
#     db.Column('id', db.Integer, db.ForeignKey('post.id'))
# )

class PostCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='post_category', lazy=True)

# class PostTag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)

class PostType(enum.Enum):
    Video = 'Video'
    Article = 'Article'
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
    category_post_id = db.Column(db.Integer, db.ForeignKey('post_category.id'), nullable=False)
    # tag = db.relationship('PostTag', secondary=post_tag, backref=db.backref('subscribers', lazy='dynamic'))

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.text}', '{self.created}')"

#db.create_all()