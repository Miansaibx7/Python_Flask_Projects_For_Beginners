from flask import Blueprint, redirect, render_template, flash, url_for, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from functools import wraps

from models.database import db, User
from forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm, ResendVerificationForm
from extensions import mail

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Access denied. Admin only.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def _generate_confirmation_token(email: str) -> str:
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt=current_app.config.get("SECURITY_PASSWORD_SALT", "email-confirm-salt"))

def _confirm_token(token: str, expiration=3600*24) -> str:
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt=current_app.config.get("SECURITY_PASSWORD_SALT", "email-confirm-salt"), max_age=expiration)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    return email

@auth_bp.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("shop.product_list"))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        username = form.username.data.strip()
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.login"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register"))
        user = User(username=username, email=email, role="customer", email_confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            current_app.logger.info(f"User {email} registered successfully")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception("DB error creating user")
            flash("An error occurred creating your account. Try again.", "danger")
            return redirect(url_for("auth.register"))
        token = _generate_confirmation_token(user.email)
        verify_url = url_for("auth.verify_email", token=token, _external=True)
        msg = Message("Verify your email", sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[user.email])
        msg.body = f"Thanks for registering. Verify your email by clicking: {verify_url}\n\nIf you didn't register, ignore this message."
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.exception("Failed to send verification email")
            flash("Account created but failed to send verification email. Contact support.", "warning")
            return redirect(url_for("auth.login"))
        flash("Registration successful! Please check your email to verify your account.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth_bp.route("/verify/<token>")
def verify_email(token):
    email = _confirm_token(token)
    if not email:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Account not found.", "danger")
        return redirect(url_for("auth.register"))
    if user.email_confirmed:
        flash("Account already confirmed. Please login.", "info")
        return redirect(url_for("auth.login"))
    user.email_confirmed = True
    user.email_confirmed_at = db.func.now()
    db.session.commit()
    current_app.logger.info(f"User {email} verified email successfully")
    flash("Email verified! You can now login.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/resend_verification", methods=["GET", "POST"])
def resend_verification():
    if current_user.is_authenticated:
        return redirect(url_for("shop.product_list"))
    form = ResendVerificationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and not user.email_confirmed:
            token = _generate_confirmation_token(user.email)
            verify_url = url_for("auth.verify_email", token=token, _external=True)
            msg = Message("Verify your email", sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[user.email])
            msg.body = f"Verify your email by clicking: {verify_url}\n\nIf you didn't register, ignore this message."
            try:
                mail.send(msg)
                flash("Verification email resent. Check your inbox.", "success")
            except Exception as e:
                current_app.logger.exception("Failed to resend verification email")
                flash("Failed to resend verification email. Contact support.", "warning")
        else:
            flash("Email not found or already verified.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("resend_verification.html", form=form)

@auth_bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("shop.product_list"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user:
            token = _generate_confirmation_token(user.email)
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            msg = Message("Password Reset Request", sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[user.email])
            msg.body = f"To reset your password, click: {reset_url}\n\nIf you didn't request this, ignore this message."
            try:
                mail.send(msg)
                flash("Password reset email sent. Check your inbox.", "success")
            except Exception as e:
                current_app.logger.exception("Failed to send reset email")
                flash("Failed to send reset email. Contact support.", "warning")
        else:
            flash("Email not found.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("reset_password_request.html", form=form)

@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = _confirm_token(token)
    if not email:
        flash("Invalid or expired reset link.", "danger")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Account not found.", "danger")
        return redirect(url_for("auth.login"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        current_app.logger.info(f"User {email} reset password successfully")
        flash("Password reset successful. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("shop.product_list"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            if not user.email_confirmed:
                flash("Please verify your email before logging in.", "warning")
                return redirect(url_for("auth.login"))
            remember = getattr(form, "remember", None)
            remember_val = False
            if remember is not None:
                remember_val = remember.data
            login_user(user, remember=remember_val)
            current_app.logger.info(f"User {email} logged in successfully")
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("shop.product_list"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    email = current_user.email
    logout_user()
    current_app.logger.info(f"User {email} logged out")
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))