from flask import Blueprint, redirect, url_for, flash, render_template
from lgblog.forms import LoginForm, RegisterForm
from os import path
from lgblog.models import User
from lgblog import db
from uuid import uuid4
from flask_login import login_user, logout_user, current_user, AnonymousUserMixin
from flask_principal import identity_changed, current_app, AnonymousIdentity

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'main')
)


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """View function for login."""

    # Will be check the account whether rigjt.
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Using the Flask-Login to processing and check the login status for user
        # Remember the user's login status.
        login_user(user, remember=form.rememberme.data)

        flash("you have been loged in ")
        return redirect(url_for('blog.home'))

    return render_template('main/login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function for logout."""

    # Using the Flask-Login to processing and check the logout status for user.
    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())

    flash("You have been logged out.", category="success")
    return redirect(url_for('blog.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
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
