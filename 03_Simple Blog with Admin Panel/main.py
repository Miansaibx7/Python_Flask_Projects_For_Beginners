from flask import Flask
from models.database import db
from routes.auth import auth
from routes.admin import admin
from routes.blog import blogs
from routes.forms import FlaskForm

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__,template_folder="templates")

app.config["SECRET_KEY"] = 'Your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
csrf = CSRFProtect(app)

app.register_blueprint(auth)
app.register_blueprint(blogs)
app.register_blueprint(admin)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
