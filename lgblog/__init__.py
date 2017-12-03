from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig
from .extensions import bcrypt

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
app.secret_key = 'nowcoder'
bcrypt.init_app(app)

from lgblog.controllers import blog, main

# Register the Blueprint into app object
app.register_blueprint(blog.blog_blueprint)
app.register_blueprint(main.main_blue_print)


@app.route('/')
def index():
    # Redirect the Request_url '/' to '/blog/'
    return redirect(url_for('blog.home'))
