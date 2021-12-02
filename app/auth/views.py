from flask import url_for, render_template, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from . import auth
from .. import db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User


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


@auth.route("/account")
@login_required
def account():
    return render_template('auth/account.html', user=current_user)