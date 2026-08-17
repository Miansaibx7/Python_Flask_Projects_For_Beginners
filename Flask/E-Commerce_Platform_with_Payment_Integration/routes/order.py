from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.database import Order

order_bp = Blueprint("order", __name__, template_folder="../templates")

@order_bp.route("/history")
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("order_history.html", orders=orders)