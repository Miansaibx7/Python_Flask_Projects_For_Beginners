from flask import Blueprint, render_template, request
from extensions import db
from models.database import Product

shop_bp = Blueprint("shop", __name__, template_folder="../templates")

@shop_bp.route("/")
@shop_bp.route("/products")
def product_list():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    query = Product.query
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%") |
            Product.description.ilike(f"%{search}%")
        )
    if category:
        query = query.filter_by(category=category)

    products = query.paginate(page=page, per_page=10)
    categories = db.session.query(Product.category).distinct().all()

    return render_template(
        "product_list.html",
        products=products,
        categories=categories,
        search=search,
        category=category
    )

@shop_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)
