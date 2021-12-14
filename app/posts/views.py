import os
import secrets

from PIL import Image
from flask import url_for, render_template, flash, redirect, current_app, request
from .forms import CreatePost, CategoryForm
from . import posts
from .models import Post, PostCategory
from .. import db
from flask_login import current_user, login_required


@posts.route('/', methods=['GET', 'POST'])
def home():
    page = request.args.get('page')
    posts = Post.query.order_by(Post.category_post_id)

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=3)

    return render_template('posts/home.html', pages=pages)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePost()
    form.category.choices = [(category.id, category.name) for category in PostCategory.query.all()]

    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
        else:
            picture_file = 'post_default.jpg'

        post = Post(title=form.title.data,
                    text=form.text.data,
                    image_file=picture_file,
                    type=form.type.data,
                    enabled=form.enabled.data,
                    user_id=current_user.id,
                    category_post_id=form.category.data)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.home'))

    return render_template('posts/create.html', form=form)


@posts.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)

    if current_user.id != post.user_id:
        flash('This is not your post', category='warning')
        return redirect(url_for('posts.detail', pk=post))

    form = CreatePost()
    form.category.choices = [(category.id, category.name) for category in PostCategory.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.enabled = form.enabled.data
        post.image_file = save_picture(form.image.data) if form.image.data else 'post_default.jpg'
        post.category_post_id = form.category.data

        db.session.add(post)
        db.session.commit()

        flash('Post has been update', category='success')
        return redirect(url_for('posts.detail', id=id, pk=post))

    form.title.data = post.title
    form.text.data = post.text
    form.type.data = post.type
    form.enabled.data = post.enabled
    form.image.data = post.image_file
    form.category.data = post.category_post_id

    return render_template('posts/create.html', form=form)


@posts.route('/<id>', methods=['GET', 'POST'])
def detail(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail.html', pk=post)


@posts.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        flash('Post has been delete', category='success')
        return redirect(url_for('posts.home'))

    flash('This is not your post', category='warning')
    return redirect(url_for('posts.detail', pk=id))


@posts.route('/create_category', methods=['GET', 'POST'])
@login_required
def category_crud():
    form = CategoryForm()

    if form.validate_on_submit():
        category = PostCategory(name=form.name.data)

        db.session.add(category)
        db.session.commit()
        flash('Add success', category='success')
        return redirect(url_for('.category_crud'))

    categories = PostCategory.query.all()
    return render_template('posts/category_crud.html', categories=categories, form=form)


@posts.route('/update_category/<id>', methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = PostCategory.query.get_or_404(id)
    form = CategoryForm()

    if form.validate_on_submit():
        category.name = form.name.data

        db.session.add(category)
        db.session.commit()
        flash('Success', category='success')
        return redirect(url_for('.category_crud'))

    form.name.data = category.amount_ram
    categories = PostCategory.query.all()

    return render_template('posts/category_crud.html', categories=categories, form=form)


@posts.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_category(id):
    category = PostCategory.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash('Category delete', category='success')
    return redirect(url_for('.category_crud'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static//post_pics', picture_fn)
    output_size = (150, 150)

    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn
