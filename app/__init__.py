from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object("config")
app.config["UPLOAD_FOLDER"] = "static/img"
app.jinja_env.globals.update(zip=zip)

db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=8888))

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
lm.login_message_category = "info"

from app.controllers import routes
from app.models import tables
