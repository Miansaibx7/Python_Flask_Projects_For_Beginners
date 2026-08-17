from flask import Flask
from config import Config
from extensions import db, login_manager, mail, limiter
from models.database import User  # Import your User model
from routes.auth import auth_bp
from routes.shop import shop_bp
from routes.cart import cart_bp
from routes.payment import payment_bp
from routes.admin import admin_bp
from routes.order import order_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    # Configure Flask-Login user loader (only here)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(payment_bp, url_prefix="/payment")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(order_bp, url_prefix="/order")

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG)