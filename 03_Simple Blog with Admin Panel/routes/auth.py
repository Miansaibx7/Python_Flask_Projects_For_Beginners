from flask import Blueprint,render_template,redirect,url_for,flash,request,session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db,User
from routes.forms import RegistrationForm,LogInForm

auth = Blueprint('auth',__name__)

@auth.route('/')
def home():
    return redirect(url_for('auth.register'))

@auth.route('/register',methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("auth.login"))
        
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(name= form.name.data, email= form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)



@auth.route("/login",methods=['POST','GET'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("User not registered. Please register first.", "warning")
            return redirect(url_for('auth.register'))
        
        if user and check_password_hash(user.password,form.password.data):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash(f"Welcome, {user.name}!", "success")
            return redirect(url_for("blogs.blog_page"))
        else:
           flash("Invalid login credentials", "danger")
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('is_admin', None) 
    flash("Logged out", "info")
    return redirect(url_for('auth.login'))