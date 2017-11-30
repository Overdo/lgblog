
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('config/app.conf')
db = SQLAlchemy(app)
app.secret_key = 'nowcoder'

from lgblog import views, models
