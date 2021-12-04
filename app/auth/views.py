import os
import secrets

from flask import url_for, render_template, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from . import auth
from .. import db, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from .models import User
from datetime import datetime
from PIL import Image


@auth.route('/')
def home():
    return redirect(url_for('home'))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already loggined in!', category='warning')
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=bcrypt.generate_password_hash(str(form.password.data)),
                    image_file='default.jpg')

        db.session.add(user)
        db.session.commit()

        flash(f'{form.username.data} registered!', category='success')
        login_user(user)
        return redirect(url_for('home'))

    return render_template('auth/register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already loggined in!', category='warning')
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        try:
            user_db = User.query.filter_by(email=form.email.data).first()
            is_password = bcrypt.check_password_hash(user_db.password, form.password.data)
        except AttributeError:
            flash('Invalid login or password', category='warning')
            return redirect(url_for('auth.login'))

        if form.email.data == user_db.email and is_password:
            login_user(user_db)
            flash(f'Logged in by username {user_db.username}!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Invalid login or password', category='warning')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


@auth.route("/users")
@login_required
def users():
    all_users = User.query.all()
    count = User.query.count()

    return render_template('auth/users.html',
                           all_users=all_users,
                           count=count)


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('home'))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    form_reset = ResetPasswordForm()

    if form_reset.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form_reset.new_password.data).decode('utf-8')
        db.session.commit()
        flash('Password changed', category='success')
        return redirect(url_for('auth.account'))

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash("Your accounts data are updated", category="success")

        return redirect(url_for('auth.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('auth/account.html', user=current_user, image=image, form=form, form_reset=form_reset)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static//profile_pics', picture_filename)
    output_size = (150, 150)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_filename

@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_date = datetime.utcnow()
        db.session.commit()