## project/__init__.py

from flask import Flask,render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
from project.api.views import api_blueprint


### register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404


