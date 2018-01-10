from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_cache import Cache
from flask_restful import Api
import flask_login
from flask import redirect,url_for

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

from flask_admin import Admin,expose
import flask_admin

class MyAdminIndexView(flask_admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('main.login'))
        return super(MyAdminIndexView, self).index()

# Create the Flask-Admin's instance
flask_admin = Admin(index_view=MyAdminIndexView())

# Create the Flask-Restful's instance
restful_api = Api()
