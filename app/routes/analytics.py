from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.analytics.insights import get_top_products, get_revenue_summary

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/top-products', methods=['GET'])
@jwt_required()
def top_products():
    data = get_top_products()
    return jsonify({'top_products': data}), 200


@analytics_bp.route('/revenue', methods=['GET'])
@jwt_required()
def revenue():
    data = get_revenue_summary()
    return jsonify({'revenue': data}), 200