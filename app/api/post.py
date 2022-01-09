import datetime
import jwt
# from flask_jwt_extended import jwt_required
from functools import wraps
from flask import request, jsonify, current_app, make_response
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
from .. import db, bcrypt, app
from . import api
from ..auth.models import User
from ..posts.models import Post, PostTag


post_post_args = reqparse.RequestParser()
post_post_args.add_argument("title", type=str, help="Title is required", required=True)
post_post_args.add_argument("text", type=str, help="Text is required", required=True)
post_post_args.add_argument("image_file", type=str, help="Image is required", required=True)
post_post_args.add_argument("created", type=str, help="Date is required", required=True)
post_post_args.add_argument("type", type=str, help="Type is required", required=True)
post_post_args.add_argument("enabled", type=bool, help="Enabled is required", required=True)
post_post_args.add_argument("user_id", type=int, help="User id is required", required=True)
post_post_args.add_argument("category_post_id", type=int, help="Category id is required", required=True)
post_post_args.add_argument("tag", type=str, help="Tag id is required", required=True)

post_update_args = reqparse.RequestParser()
post_update_args.add_argument("title", type=str)
post_update_args.add_argument("text", type=str)
post_update_args.add_argument("image_file", type=str)
post_update_args.add_argument("enabled", type=bool)


resourses = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    'image_file': fields.String(default='post_default.jpg'),
    'created': fields.String,
    'type': fields.String,
    'enabled': fields.Boolean,
    'user_id': fields.Integer,
    'category_post_id': fields.Integer,
    'tag': fields.String
}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()  # ???
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)
        # return f(*args, **kwargs)

    return decorated


@api.route('/v2/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify 1', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query\
        .filter_by(username=auth.username)\
        .first()

    if not user:
        return make_response('Could not verify 2', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify 3', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

#
# @api.route('/v2/unprotected')
# def unprotected():
#     return jsonify({'message': 'Anyone can view this!'})
#
#
# @api.route('/v2/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'This is only available for people with valid tokens!'})
#


class PostAllApi(Resource):
    @marshal_with(resourses)
    def get(self):
        return Post.query.all()


class PostApi(Resource):
    @marshal_with(resourses)
    def get(self, id):
        post = Post.query.get_or_404(id)

        if not post:
            abort(404, message="Could not find post with that id")

        return post

    @marshal_with(resourses)
    @token_required
    def post(self, current_user):
        data = post_post_args.parse_args()
        post_new = Post(
            title=data['title'],
            text=data['text'],
            image_file=data['image_file'],
            created=db.func.now(),
            type=data['type'],
            enabled=data['enabled'],
            user_id=current_user.id,
            category_post_id=data['category_post_id'],
            tag=data['tag'],
        )

        db.session.add(post_new)
        db.session.commit()
        return post_new, 201

    @marshal_with(resourses)
    @token_required
    def put(self, id, current_user):
        args = post_update_args.parse_args()
        post = Post.query.filter_by(id=id, user_id=current_user.id).first()

        if not post:
            abort(404, message="Post doesn`t exist, cannot update")
        if args['title']:
            post.title = args['title']
        if args['text']:
            post.text = args['text']
        if args['image_file']:
            post.image_file = args['image_file']
        if type(args['enabled']) == bool:
            post.enabled = args['enabled']

        db.session.commit()
        return post

    @token_required
    def delete(self, id, current_user):
        # p = Post.query.get(id)
        p = Post.query.filter_by(id=id, user_id=current_user.id).first()
        db.session.delete(p)
        db.session.commit()
        return jsonify({'message': 'The post has been deleted!'}), 204


api = Api(current_app)
api.add_resource(PostApi, "/api/v2/<int:id>")
api.add_resource(PostAllApi, "/api/v2/")


