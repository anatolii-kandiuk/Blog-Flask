import os
import secrets

from PIL import Image
from flask import url_for, render_template, flash, redirect, current_app
from .forms import CreatePC, CategoryForm
from . import personal_computers
from .models import Category, PersonalComputer
from .. import db
from flask_login import current_user, login_required

@personal_computers.route('/', methods=['GET', 'POST'])
def home():
    all_computers = PersonalComputer.query.order_by(PersonalComputer.firm).all()
    return render_template('personal_computers/home.html', personal_computers=all_computers)



@personal_computers.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePC()
    form.category.choices = [(category.id, category.amount_ram) for category in Category.query.all()]

    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
        else:
            picture_file = 'default_comp.jpg'

        pc = PersonalComputer(firm=form.firm.data,
                                type_processor=form.type_processor.data,
                                clock_frequency=form.clock_frequency.data,
                                is_available=form.is_available.data,
                                image_file=picture_file,
                                category_ram_id=form.category.data,
                                user_id=current_user.id,
                                date_created=form.date_created.data)

        db.session.add(pc)
        db.session.commit()

        return redirect(url_for('pc.home'))

    return render_template('personal_computers/create.html', form=form)

@personal_computers.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    pc = PersonalComputer.query.get_or_404(id)

    if current_user.id != pc.user_id:
        flash('This is not your post', category='warning')
        return redirect(url_for('pc.detail', pk=pc))

    form = CreatePC()
    form.category.choices = [(category.id, category.amount_ram) for category in Category.query.all()]

    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            image_file = picture_file
        else:
            image_file = 'default_comp.jpg'

        pc.firm = form.firm.data
        pc.type_processor = form.type_processor.data
        pc.clock_frequency = form.clock_frequency.data
        pc.is_available = form.is_available.data
        pc.category_ram_id = form.category.data
        pc.image_file = image_file

        db.session.add(pc)
        db.session.commit()

        flash('PC has been update', category='success')
        return redirect(url_for('pc.detail', id=id, pk=pc))

    form.firm.data = pc.firm
    form.type_processor.data = pc.type_processor
    form.clock_frequency.data = pc.clock_frequency
    form.is_available.data = pc.is_available
    form.image_file.data = pc.image_file
    form.category.data = pc.category_ram_id

    return render_template('personal_computers/create.html', form=form)


@personal_computers.route('/<id>', methods=['GET', 'POST'])
def detail(id):
    pc = PersonalComputer.query.get_or_404(id)
    return render_template('personal_computers/detail.html', pk=pc)


@personal_computers.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    pc = PersonalComputer.query.get_or_404(id)
    if current_user.id == pc.user_id:
        db.session.delete(pc)
        db.session.commit()
        flash('PC has been delete', category='success')
        return redirect(url_for('pc.home'))

    flash('This is not your post', category='warning')
    return redirect(url_for('pc.detail', pk=id))


@personal_computers.route('/create_ram', methods=['GET', 'POST'])
@login_required
def category_crud():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(amount_ram=form.ram.data)

        db.session.add(category)
        db.session.commit()
        flash('Add success', category='success')
        return redirect(url_for('.category_crud'))

    categories = Category.query.all()
    return render_template('personal_computers/category_crud.html', categories=categories, form=form)


@personal_computers.route('/update_category/<id>', methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()

    if form.validate_on_submit():
        category.amount_ram = form.ram.data

        db.session.add(category)
        db.session.commit()
        flash('Success', category='success')
        return redirect(url_for('.category_crud'))

    form.ram.data = category.amount_ram
    categories = Category.query.all()

    return render_template('personal_computers/category_crud.html', categories=categories, form=form)

@personal_computers.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash('Category delete', category='success')
    return redirect(url_for('.category_crud'))

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