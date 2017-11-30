
from lgblog import app, db
from flask import render_template, redirect


@app.route('/')
def index():
    return render_template('index.html')


















