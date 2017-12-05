from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig
from .extensions import bcrypt,login_manager
from lgblog.extensions import principals
from flask_principal import identity_loaded,identity_changed,RoleNeed,UserNeed
from flask_login import current_user


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
app.secret_key = 'nowcoder'
bcrypt.init_app(app)
login_manager.init_app(app)

from lgblog.controllers import blog, main

# Register the Blueprint into app object
app.register_blueprint(blog.blog_blueprint)
app.register_blueprint(main.main_blueprint)


@app.route('/')
def index():
    # Redirect the Request_url '/' to '/blog/'
    return redirect(url_for('blog.home'))


principals.init_app(app)
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """Change the role via add the Need object into Role.

       Need the access the app object.
    """

    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity user object
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Add each role to the identity user object
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
