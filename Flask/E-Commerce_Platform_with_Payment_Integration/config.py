import os
from datetime import timedelta

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set. Add SECRET_KEY to your .env file.")

    # Security
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    if not SECURITY_PASSWORD_SALT:
        raise RuntimeError(
            "SECURITY_PASSWORD_SALT is not set. "
            "Add SECURITY_PASSWORD_SALT to your .env file."
        )

    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URI is not set. Add DATABASE_URI to your .env file.")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    if not MAIL_USERNAME:
        raise RuntimeError("MAIL_USERNAME is not set. Add MAIL_USERNAME to your .env file.")

    if not MAIL_PASSWORD:
        raise RuntimeError("MAIL_PASSWORD is not set. Add MAIL_PASSWORD to your .env file.")

    if not MAIL_DEFAULT_SENDER:
        raise RuntimeError("MAIL_DEFAULT_SENDER is not set. Add MAIL_DEFAULT_SENDER to your .env file.")

    # Stripe
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

    if not STRIPE_SECRET_KEY:
        raise RuntimeError("STRIPE_SECRET_KEY is not set. Add STRIPE_SECRET_KEY to your .env file.")

    if not STRIPE_PUBLISHABLE_KEY:
        raise RuntimeError("STRIPE_PUBLISHABLE_KEY is not set. Add STRIPE_PUBLISHABLE_KEY to your .env file.")

    # Application
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"