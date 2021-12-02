from flask import url_for, render_template, flash, redirect
from flask_login import login_user, current_user
from . import form
from .. import db, bcrypt
from .forms import RegistrationForm
from .models import User

@form.route('/')
def home():
    return redirect(url_for('home'))

@form.route("/register", methods=['GET', 'POST'])
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



