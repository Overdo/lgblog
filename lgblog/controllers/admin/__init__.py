from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from lgblog.forms import CKTextAreaField
import flask_login
from flask import redirect, url_for


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    def is_accessible(self):
        return flask_login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class PostView(CustomModelView):
    """View function of Flask-Admin for Post create/edit Page includedin Models page"""

    def is_accessible(self):
        return flask_login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    # Using the CKTextAreaField to replace the Field name is `test`
    form_overrides = dict(text=CKTextAreaField)

    # Using Search box
    column_searchable_list = ('text', 'title')

    # Using Add Filter box
    column_filters = ('publish_date',)

    # Custom the template for PostView
    # Using js Editor of CKeditor
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'

