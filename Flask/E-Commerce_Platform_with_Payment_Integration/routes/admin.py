from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from routes.auth import admin_required
from models.database import db, Product, Order
from forms import ProductForm

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route("/products", methods=["GET", "POST"])
@login_required
@admin_required
def manage_products():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category=form.category.data
        )
        db.session.add(product)
        try:
            db.session.commit()
            flash("Product added successfully.", "success")
        except Exception as e:
            db.session.rollback()
            flash("Error adding product.", "danger")
        return redirect(url_for("admin.manage_products"))
    products = Product.query.all()
    return render_template("manage_products.html", form=form, products=products)

@admin_bp.route("/orders")
@login_required
@admin_required
def manage_orders():
    orders = Order.query.all()
    return render_template("manage_orders.html", orders=orders)