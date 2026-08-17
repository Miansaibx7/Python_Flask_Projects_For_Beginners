from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.database import db, Cart, CartItem, Product

cart_bp = Blueprint("cart", __name__, template_folder="../templates")

@cart_bp.route("/")
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    return render_template("cart.html", cart=cart)

@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    quantity = request.form.get("quantity", 1, type=int)
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        flash("Not enough stock available.", "danger")
        return redirect(url_for("shop.product_detail", product_id=product_id))
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    try:
        db.session.commit()
        flash("Item added to cart.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error adding item to cart.", "danger")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/remove/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("cart.view_cart"))
    db.session.delete(cart_item)
    db.session.commit()
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart.view_cart"))