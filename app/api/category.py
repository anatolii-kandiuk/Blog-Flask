from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from .. import db, bcrypt
from functools import wraps
from ..posts.models import PostCategory
from . import api
from ..auth.models import User


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return jsonify({'message': 'Need authorization'}), 401

        try:
            user_db = User.query.filter_by(email=auth.username).first()
            is_password = bcrypt.check_password_hash(user_db.password, auth.password)
        except AttributeError:
            return jsonify({'message': 'Invalid login or password'})

        if is_password:
            return f(*args, **kwargs)

        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@api.route('/category', methods=['GET'])
@protected
def get_categories():
    categories = PostCategory.query.all()
    categories_json = []

    for category in categories:
        category_dict = {}
        category_dict['id'] = category.id
        category_dict['name'] = category.name
        categories_json.append(category_dict)

    return jsonify({'categories': categories_json})


@api.route('/category/<int:category_id>', methods=['GET'])
@protected
def get_category(category_id):
    category = PostCategory.query.get_or_404(category_id)

    if not category:
        return jsonify({'message': 'Not key name'}), 404

    return jsonify({'category':
                    {'id': category.id,
                     'name': category.name}}), 201


@api.route('/category', methods=['POST'])
@protected
def add_category():
    name = request.get_json()['category']['name']

    if not name:
        return jsonify({'message': 'Not key name'}), 422

    category = PostCategory.query.filter_by(name=name).first()

    if category:
        return jsonify({'message': f'The category "{name}" already exist!'})

    new_category = PostCategory(name=name)

    try:
        db.session.add(new_category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'DB ERROR'})

    return get_category(new_category.id)


@api.route('/category/<int:category_id>', methods=['PUT'])
@protected
def edit_category(category_id):
    name = request.get_json()['category']['name']

    if not name:
        return jsonify({'message': 'Not key name'})

    category = PostCategory.query.filter_by(name=name).first()

    if category:
        return jsonify({'message': f'The category "{name}" already exist!'})

    category = PostCategory.query.get_or_404(category_id)

    if not category:
        return jsonify({'message': 'Category does not exist'}), 404

    category.name = name
    db.session.commit()

    return jsonify({'category':
                    {'id': category.id,
                     'name': category.name}}), 201


@api.route('/category/<int:category_id>', methods=['DELETE'])
@protected
def delete_category(category_id):
    category = PostCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'The category has been deleted!'})