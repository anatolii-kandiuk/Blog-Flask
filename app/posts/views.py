import os
import secrets

from PIL import Image
from flask import url_for, render_template, flash, redirect, current_app
from .forms import CreatePost
from . import posts
from .models import Post
from .. import db
from flask_login import current_user, login_required

@posts.route('/', methods=['GET', 'POST'])
def home():
    posts = Post.query.order_by(Post.type).all()
    return render_template('posts/home.html', posts=posts)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePost()

    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_picture(form.image_file.data)
        else:
            image_file = 'post_default.jpg'

        post = Post(title=form.title.data,
                    text=form.text.data,
                    image_file=image_file,
                    type=form.type.data,
                    enabled=form.enabled.data,
                    user_id=current_user.id)

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

    if form.validate_on_submit():
        if form.image_file.data:
            picture = save_picture(form.image_file.data)
            image_file = picture
        else:
            image_file = 'post_default.jpg'

        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.enabled = form.enabled.data
        post.image_file = image_file

        db.session.add(post)
        db.session.commit()

        flash('Post has been update', category='success')
        return redirect(url_for('posts.detail', id=id, pk=post))

    form.title.data = post.title
    form.text.data = post.text
    form.type.data = post.type
    form.enabled.data = post.enabled
    form.image_file.data = post.image_file

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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static//profile_pics', picture_fn)
    output_size = (250, 250)

    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn