from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_cache import Cache


bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "please login to access this page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(userid):
    '''load the user info'''
    from lgblog.models import User

    return User.query.filter_by(id=userid).first()


# Create the Flask-Principal's instance
principals = Principal()

# 这里设定了 3 种权限, 这些权限会被绑定到 Identity 之后才会发挥作用.
# Init the role permission via RoleNeed(Need).
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

# Create the Flask-Cache's instance
cache = Cache()
