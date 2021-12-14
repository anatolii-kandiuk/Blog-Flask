from flask import request, jsonify
from .. import db
from functools import wraps

from ..posts.models import PostCategory
from . import api

api_username = 'admin'
api_password = 'admin'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username \
           and auth.password == api_password:
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
        return jsonify({'message': 'Not key name'})

    categories = PostCategory.query.all()

    for category in categories:
        if category.name == name:
            return jsonify({'message': f'The category "{name}" already exist!'})

    new_category = PostCategory(name=name)

    db.session.add(new_category)
    db.session.commit()

    return get_category(new_category.id)


@api.route('/category/<int:category_id>', methods=['PUT'])
@protected
def edit_category(category_id):
    name = request.get_json()['category']['name']

    if not name:
        return jsonify({'message': 'Not key name'})

    categories = PostCategory.query.all()

    if not PostCategory.query.get_or_404(category_id):
        return jsonify({'message': 'Category does not exist'}), 404

    for category in categories:
        if category.name == name:
            return jsonify({'message': f'The category "{name}" already exist!'})

    category = PostCategory.query.get_or_404(category_id)
    category.name = name
    db.session.commit()

    return jsonify({'category':
                    {'id': category.id,
                     'name': category.name}})


@api.route('/category/<int:category_id>', methods=['DELETE'])
@protected
def delete_category(category_id):
    category = PostCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'The category has been deleted!'})