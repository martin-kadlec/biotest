import os
from flask import Flask, render_template, request, url_for, redirect
from models import db, Guess, Image
from pathlib import Path
import random

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

def add_images():
    with app.app_context():
        img_path = Path(os.path.dirname(__file__)) / "img"
        images = [i.name for i in img_path.glob("*.png")]
        db_images = set((i.filename for i in Image.query.all()))

        for image in images:
            if not image in db_images:
                new = Image()
                new.filename = image
                new.title = f"unknown - {image}"
                db.session.add(new)

        db.session.commit()

# views

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rand")
def rand():
    images = Image.query.all()
    rimg = images[random.randint(0, len(images)-1)]
    return render_template("guess.html", img=rimg)
