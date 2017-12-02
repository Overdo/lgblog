from os import path

from flask import render_template, Blueprint, redirect, url_for

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder=path.join('templates/blog'),
    url_prefix='/blog')

