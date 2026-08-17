from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models.database import db, Cart, Order, OrderItem
from forms import CheckoutForm
import stripe

payment_bp = Blueprint("payment", __name__, template_folder="../templates")

@payment_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash("Your cart is empty.", "danger")
        return redirect(url_for("cart.view_cart"))
    form = CheckoutForm()
    if form.validate_on_submit():
        total = sum(item.product.price * item.quantity for item in cart.items)
        stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": item.product.name},
                            "unit_amount": int(item.product.price * 100),
                        },
                        "quantity": item.quantity,
                    }
                    for item in cart.items
                ],
                mode="payment",
                success_url=url_for("payment.order_confirmation", _external=True),
                cancel_url=url_for("payment.checkout", _external=True),
            )
            order = Order(user_id=current_user.id, total=total, status="pending")
            db.session.add(order)
            db.session.flush()
            for item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.product.price
                )
                db.session.add(order_item)
                item.product.stock -= item.quantity
            db.session.delete(cart)
            db.session.commit()
            return redirect(session.url)
        except Exception as e:
            current_app.logger.exception("Payment processing error")
            flash("Error processing payment.", "danger")
    return render_template("checkout.html", form=form, cart=cart, stripe_publishable_key=current_app.config["STRIPE_PUBLISHABLE_KEY"])

@payment_bp.route("/order_confirmation")
@login_required
def order_confirmation():
    flash("Payment successful! Order placed.", "success")
    return render_template("order_confirmation.html")