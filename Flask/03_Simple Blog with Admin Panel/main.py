import os
from flask import Flask
from models.database import db
from routes.auth import auth
from routes.admin import admin
from routes.blog import blogs
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

app = Flask(__name__, template_folder="templates")

# Config class for environment variables
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Apply config
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(blogs)
app.register_blueprint(admin)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
