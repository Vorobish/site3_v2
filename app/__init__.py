from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_flask.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import models

# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
# flask db --help
