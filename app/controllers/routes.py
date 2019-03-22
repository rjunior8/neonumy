# -*- coding: utf-8 -*-

from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug import generate_password_hash, check_password_hash
import uuid
import os
from PIL import Image

from app import app, db, lm
from app.models.tables import Users, Images
from app.models.forms import RegisterForm, LoginForm, UploadPictureForm


@app.route("/register", methods=["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for("home"))
  reg_form = RegisterForm()
  if reg_form.validate_on_submit():
    user_prot = str(uuid.uuid4()).split('-')[0]
    hashed_password = generate_password_hash(reg_form.password.data)
    user = Users(id=None,
                 username=reg_form.username.data,
                 email=reg_form.email.data,
                 password=hashed_password,
                 user_prot=user_prot)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("login"))
  return render_template("register.html", reg_form=reg_form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("home"))
  login_form = LoginForm()
  if login_form.validate_on_submit():
    user = Users.query.filter((Users.username == login_form.login.data) | (Users.email == login_form.login.data)).first()
    if user:
      check = check_password_hash(user.password, login_form.password.data)
      if check:
        login_user(user)
        next_page = request.args.get("next")
        flash("Login Successfully!", "success")
        return redirect(next_page) if next_page else redirect(url_for("home"))
      else:
        flash("Incorrect Password!", "danger")
    else:
      flash("Incorrect User!", "danger")
  return render_template("login.html", login_form=login_form)

def save_picture(form_picture):
  random_hex = uuid.uuid4().hex
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, "static/pics", picture_fn)

  output_size = (1920, 1080)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)

  return picture_fn

@app.route('/')
@app.route("/home")
def home():
  if not current_user.is_authenticated:
    return redirect(url_for("login"))
  images = Images.query.filter_by(user_id=current_user.id).all()
  return render_template("all_images.html", images=images)

@app.route("/upload-image", methods=["GET", "POST"])
def upload_img():
  img_form = UploadPictureForm()
  if img_form.validate_on_submit():
    if img_form.picture.data:
      picture_file = save_picture(img_form.picture.data)
      img = Images(id=None, image_file=picture_file, user_id=current_user.id)
      db.session.add(img)
      db.session.commit()
      flash("Image Uploaded Successfully!", "success")
  return render_template("upload_image.html", img_form=img_form)

@app.route("/delete-image", methods=["POST"])
def delete_img():
  try:
    _id = request.form["id"]
    img = Images.query.filter_by(id=_id).first()
    db.session.delete(img)
    db.session.commit()
    return jsonify({"result" : "success"})
  except Exception as e:
    return jsonify({"result" : "failure"})

@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("You has left.", "info")
  return redirect(url_for("login"))