from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed

from app.models.tables import Users


class RegisterForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
  submit = SubmitField("Save")

  def validate_username(self, username):
    user = Users.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("That username is taken. Please choose a different one.")

  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("That email is taken. Please choose a different one.")

class LoginForm(FlaskForm):
  login = StringField("Username or Email", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")

class UploadPictureForm(FlaskForm):
  picture = FileField("Upload an image", validators=[FileAllowed(["jpg", "png"])])
  submit = SubmitField("Upload")