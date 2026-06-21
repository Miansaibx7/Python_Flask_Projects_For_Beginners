from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models.database import db, User, Blog
from routes.forms import BlogForm
from functools import wraps

admin = Blueprint('admin', __name__)

# Decorator to protect admin-only routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin Dashboard
@admin.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.with_entities(User.name, User.id, User.is_admin).all()
    blogs = Blog.query.order_by(Blog.date.desc()).limit(5).all()
    return render_template('dashboard.html', users=users, blogs=blogs)

# Promote user to admin
@admin.route('/admin/promote/<int:user_id>')
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f"{user.name} has been promoted to admin.", "success")
    return redirect(url_for('admin.admin_dashboard'))

# Edit blog via admin dashboard
@admin.route('/admin/edit/<int:blog_id>', methods=['GET', 'POST'])
@admin_required
def edit_blog_admin(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm(obj=blog)

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash("Blog updated successfully!", "success")
        return redirect(url_for('admin.admin_dashboard'))

    users = User.query.with_entities(User.name, User.id, User.is_admin).all()
    blogs = Blog.query.order_by(Blog.date.desc()).limit(5).all()
    return render_template('dashboard.html', users=users, blogs=blogs, form=form, blog=blog)
