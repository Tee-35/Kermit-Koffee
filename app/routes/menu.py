from flask import Blueprint, jsonify
from app.models.product import Product

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu():
    products = Product.query.all()

    menu = []
    for product in products:
        menu.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'description': product.description
        })

    return jsonify({'menu': menu}), 200