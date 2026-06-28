from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def place_order():
    customer_id = get_jwt_identity()
    data = request.get_json()
    items = data.get['items']

    if not items:
        return jsonify({'error': 'No items provided'}), 400

    total = 0
    order_items = []

    for item in items:
        product = Product.query.get(item.get('product_id'))
        if not product:
            return jsonify({'error': f'Product {item.get("product_id")} not found'}), 404
        quantity = item.get('quantity', 1)
        total += product.price * quantity
        order_items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': product.price
        })

    order = Order(customer_id=customer_id, total_amount=round(total, 2))
    db.session.add(order)
    db.session.flush()

    for item in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product'].id,
            quantity=item['quantity'],
            unit_price=item['unit_price']
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify({
        'message': 'Order placed successfully',
        'order_id': order.id,
        'total': order.total_amount
    }), 201


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    customer_id = get_jwt_identity()
    orders = Order.query.filter_by(customer_id=customer_id).all()

    result = []
    for order in orders:
        items = []
        for item in order.order_items:
            items.append({
                'product': item.product.name,
                'quantity': item.quantity,
                'unit_price': item.unit_price
            })
        result.append({
            'order_id': order.id,
            'total': order.total_amount,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'items': items
        })

    return jsonify({'orders': result}), 200