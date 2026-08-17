from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models.database import db, Blog, User
from routes.forms import BlogForm

blogs = Blueprint("blogs", __name__)

# Main blog page: create + show all blogs
@blogs.route("/blogs", methods=['POST', 'GET'])
def blog_page():
    if 'user_id' not in session:
        flash("Please log in to view or post blogs.", "warning")
        return redirect(url_for("auth.login"))
    
    form = BlogForm()
    user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        new_blog = Blog(title=form.title.data, content=form.content.data, author=user)
        db.session.add(new_blog)
        db.session.commit()
        flash("Blog posted successfully!", "success")
        return redirect(url_for('blogs.blog_page'))
    
    # Show all blogs (newest first)
    all_blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template("blogs.html", form=form, blogs=all_blogs)

# Edit blog post (admin only)
@blogs.route("/blogs/edit/<int:blog_id>", methods=['GET', 'POST'])
def edit_blog(blog_id):
    if "user_id" not in session:
        flash('You need to log in to edit blogs.', 'warning')
        return redirect(url_for('auth.login'))
    
    if not session.get('is_admin'):
        flash("Only admins can edit blog posts.", "danger")
        return redirect(url_for('blogs.blog_page'))

    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm(obj=blog)

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash("Blog updated successfully.", "success")
        return redirect(url_for("blogs.blog_page"))
    
    return render_template("edit_post.html", form=form, blog=blog)

# Delete blog post (admin only)
@blogs.route("/blogs/delete/<int:blog_id>", methods=['POST'])
def delete_blog(blog_id):
    if 'user_id' not in session:
        flash("You need to log in to delete blogs.", "warning")
        return redirect(url_for('auth.login'))
    
    if not session.get("is_admin"):
        flash("Only admins can delete blog posts.", "danger")
        return redirect(url_for('blogs.blog_page'))
    
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted successfully.", "success")
    return redirect(url_for("blogs.blog_page"))
