from flask_login import UserMixin
from datetime import datetime

from app import db, lm


class Users(db.Model, UserMixin):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  user_prot = db.Column(db.String(8), nullable=False)

  @property
  def is_authenticated(self):
    return True

  @property
  def is_active(self):
    return True

  @property
  def is_anonymous(self):
    return False

  def get_id(self):
    return str(self.id)

  def __init__(self, id, username, email, password, user_prot):
    self.id = id
    self.username = username
    self.email = email
    self.password = password
    self.user_prot = user_prot

  def __repr__(self):
    return "{}".format(self.id)

@lm.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))

class Images(db.Model):
  __tablename__ = "images"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  image_file = db.Column(db.String(38), nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  user = db.relationship("Users", foreign_keys=user_id)

  def __init__(self, id, image_file, user_id):
    self.id = id
    self.image_file = image_file
    self.user_id = user_id

  def __repr__(self):
    return "{}".format(self.id)