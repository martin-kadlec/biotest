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
        img_path = Path(os.path.dirname(__file__)) / "static" / "img"
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

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/reset")
def reset():
    reset_db()
    add_images()
    return redirect("/rand")
    
@app.route("/rand")
def rand():
    images = Image.query.all()
    guesses = Guess.query.all()

    ii = [i.id for i in images]
    gpi = [g.image_id for g in guesses if g.passed == 1]
    gfi = [g.image_id for g in guesses if g.passed == 0]

    missing = [i for i in ii if not i in gpi and not i in gfi]

    failed = [i for i in ii if i in gfi]

    all = ii + 5*missing + 20*failed

    rid = all[random.randint(0, len(all)-1)]
    rimg = db.get_or_404(Image, rid)
    return render_template("guess.html", img=rimg)

@app.route("/check/<int:image_id>")
def check(image_id: int):
    image = db.get_or_404(Image, image_id)
    return render_template("check.html", img=image)

@app.route("/vim/<int:image_id>/<int:vim>")
def vim(image_id: int, vim: int):
    guess = Guess()
    guess.image_id = image_id
    guess.passed = vim
    
    db.session.add(guess)
    db.session.commit()

    return redirect("/rand")

@app.route("/rename/<int:image_id>", methods=["GET", "POST"])
def rename(image_id: int):
    if request.method == "POST":
        image = db.get_or_404(Image, image_id)
        image.title = request.form["title"]
        db.session.commit()
        return redirect(f"/vim/{image_id}/0")
    if request.method == "GET":
        image = db.get_or_404(Image, image_id)
        return render_template("rename.html", img=image)
    
@app.route("/worst")
def worst():
    images = Image.query.all()
    guesses = Guess.query.all()

    ii = [i.id for i in images]
    gpi = [g.image_id for g in guesses if g.passed == 1]
    gfi = [g.image_id for g in guesses if g.passed == 0]

    missing = [i for i in ii if not i in gpi and not i in gfi]

    failed = [i for i in ii if i in gfi]

    worst = [(db.get_or_404(Image, i), gfi.count(i), gpi.count(i)) for i in ii]
    worst = sorted(worst, key=lambda x: 20*x[1]-x[2], reverse=True)

    return render_template("worst.html", worst=worst)


