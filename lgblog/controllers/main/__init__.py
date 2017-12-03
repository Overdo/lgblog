from flask import Blueprint, redirect, url_for, flash, render_template
from lgblog.forms import LoginForm, RegisterForm
from os import path
from lgblog.models import User
from lgblog import db
from uuid import uuid4

main_blue_print = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'main')
)


@main_blue_print.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blue_print.route('/login/', methods=['GET', 'POST'])
def login():
    """View function for login."""

    # Will be check the account whether rigjt.
    form = LoginForm()

    if form.validate_on_submit():
        flash("you have been loged in ", category=success)
        return redirect(url_for('blog.home'))

    return render_template('main/login.html', form=form)


@main_blue_print.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function for logout."""

    flash("You have been logged out.", category="success")
    return redirect(url_for('blog.home'))


@main_blue_print.route('/register', methods=['GET', 'POST'])
def register():
    """View function for Register."""

    # Will be check the username whether exist.
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(id=str(uuid4()),
                        username=form.username.data,
                        password=form.password.data)

        db.session.add(new_user)
        db.session.commit()
        flash('Your user has been created, please login.',
              category="success")

        return redirect(url_for('main.login'))
    return render_template('main/register.html',
                           form=form)
