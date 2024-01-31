import os
from flask import Flask, render_template, request, url_for, redirect
from models import db, Test

# init app and db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# init db
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

def init_db():
    with app.app_context():
        db.create_all()

# views

@app.route("/")
def index():
    return render_template("index.html")
