import pandas as pd
from sqlalchemy import text
from app import db

def get_top_products():
    query = text("""
        SELECT p.name, SUM(oi.quantity) as total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.name
        ORDER BY total_sold DESC
    """)
    result = db.session.execute(query)
    df = pd.DataFrame(result.fetchall(), columns=['product', 'total_sold'])
    return df.to_dict(orient='records')


def get_revenue_summary():
    query = text("""
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as average_order_value
        FROM orders
    """)
    result = db.session.execute(query)
    row = result.fetchone()
    return {
        'total_orders': row[0],
        'total_revenue': round(row[1], 2),
        'average_order_value': round(row[2], 2)
    }