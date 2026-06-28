import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from werkzeug.security import generate_password_hash
import random
import time

app = create_app()

FAKE_CUSTOMERS = [
    {'username': 'marcus_j', 'email': 'marcus@koffee.com'},
    {'username': 'priya_k', 'email': 'priya@koffee.com'},
    {'username': 'sophie_t', 'email': 'sophie@koffee.com'},
    {'username': 'dan_w', 'email': 'dan@koffee.com'},
    {'username': 'aisha_m', 'email': 'aisha@koffee.com'},
    {'username': 'leo_b', 'email': 'leo@koffee.com'},
    {'username': 'nina_r', 'email': 'nina@koffee.com'},
    {'username': 'omar_s', 'email': 'omar@koffee.com'},
]

def seed_customers():
    with app.app_context():
        for c in FAKE_CUSTOMERS:
            exists = Customer.query.filter_by(email=c['email']).first()
            if not exists:
                customer = Customer(
                    username=c['username'],
                    email=c['email'],
                    password_hash=generate_password_hash('password123')
                )
                db.session.add(customer)
        db.session.commit()
        print(f"✅ Customers seeded")

def place_random_order():
    with app.app_context():
        customers = Customer.query.all()
        products = Product.query.all()

        if not customers or not products:
            print("No customers or products found")
            return

        customer = random.choice(customers)
        num_items = random.randint(1, 3)
        selected = random.sample(products, min(num_items, len(products)))

        total = 0
        order_items = []

        for product in selected:
            quantity = random.randint(1, 2)
            total += product.price * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': product.price
            })

        order = Order(
            customer_id=customer.id,
            total_amount=round(total, 2)
        )
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

        items_summary = ', '.join([f"{i['quantity']}x {i['product'].name}" for i in order_items])
        print(f"🐸 Order placed — {customer.username}: {items_summary} — £{order.total_amount}")

if __name__ == '__main__':
    print("🐸 Kermit Koffee Order Simulator starting...")
    seed_customers()

    orders_to_place = 20
    print(f"Placing {orders_to_place} random orders...\n")

    for i in range(orders_to_place):
        place_random_order()
        time.sleep(0.5)

    print(f"\n✅ Simulator complete")