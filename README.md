# Kermit Koffee 🐸

A Flask REST API backend for the Kermit Koffee membership system — built to demonstrate real-world backend development skills including authentication, relational database design, order management, and a pandas-powered analytics layer.

> **Portfolio context:** Kermit Koffee is a fictional independent coffee shop with a membership app. This project is the backend API that powers it — the engine underneath the customer-facing experience. It is built as a standalone system, fully self-contained, and designed to be extensible into a real product.

---

## Project Objective

Design and build a production-style REST API backend for a fictional coffee shop membership system. The API handles user authentication, menu management, order processing, and exposes a live analytics layer — the kind of backend a data analyst or junior developer would be expected to understand, extend, and maintain in a real role.

---

## The Concept 🐸

When a customer walks into Kermit Koffee, the barista asks:

> *"Do you have the Kermit Koffee app?"*

The customer opens the app, the barista scans their membership, and the order is logged against their account — points tracked, history saved, promotions applied automatically.

This project is the backend that makes that possible. The API receives requests from any client (a mobile app, a POS system, a web dashboard), processes them, stores the data, and serves it back. No frontend is included — this is the engine, not the interface.

---

## What Is Being Built

A Flask backend application with the following capability:

**Authentication**
- Customer registration and login
- JWT (JSON Web Token) based authentication
- Protected routes that require a valid token

**Menu Management**
- View all available products
- Products stored in a relational database with name, price, and category

**Order System**
- Authenticated customers can place orders
- Orders are linked to customers and contain one or many items
- Order history is retrievable per customer

**Analytics Layer**
- Top selling products by volume
- Total revenue figures
- Data served via dedicated analytics endpoints using pandas

**Order Simulator 🐸**
- A background script that generates random customers and places random orders at intervals
- Keeps the system live and populated — useful for demos and testing

---

## The Problem It Solves

A coffee shop running a membership scheme needs more than insights from historical data. It needs a live operational system:

- A secure way to register and authenticate customers
- A database that records every order as it happens
- An API that any client system can talk to
- An analytics layer that surfaces business metrics on demand

This project builds that operational backbone.

---

## Who It Is For

**As a portfolio piece**, this project is for hiring managers, technical leads, and recruiters evaluating backend and data engineering candidates. It demonstrates the ability to:

- Architect a multi-layered backend system
- Write clean, maintainable Python
- Work with relational databases via an ORM
- Implement authentication securely
- Integrate a data processing layer into a web application

**In a real-world context**, this API would be used by:

- A customer-facing mobile app (the Kermit Koffee app)
- A staff POS system placing and retrieving orders
- A management dashboard querying analytics endpoints

---

## How It Is Used

The API is consumed over HTTP. All requests and responses use JSON.

**Example flow:**

1. A customer registers via `POST /auth/register`
2. They log in via `POST /auth/login` and receive a JWT token
3. They include that token in the header of subsequent requests
4. They browse the menu via `GET /menu`
5. They place an order via `POST /orders`
6. Management queries `GET /analytics/top-products` to see what is selling

No frontend is included — the API is tested and demonstrated via Postman or curl, and all endpoint behaviour is documented here.

---

## Build Stages

This project is structured to reflect a realistic development workflow — not a perfect system delivered in one go. The build progresses through three stages visible in the Git commit history:

**Stage 1 — Foundation**
Set up the application structure, database models, and core routes. The system works but has rough edges: minimal error handling, no input validation, basic responses.

**Stage 2 — Fix**
Identify and resolve the issues introduced in Stage 1. Add proper error responses, handle edge cases, validate incoming data, prevent bad data reaching the database.

**Stage 3 — Improve**
Refactor for clarity and maintainability. Add the analytics layer. Add the order simulator. Improve response consistency. Document all endpoints.

This staged approach deliberately mirrors what a developer does when inheriting or extending a real codebase.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-JWT-Extended |
| Database | MySQL (local) |
| Analytics | pandas |
| Environment | python-dotenv |
| Driver | PyMySQL |

---

## Project Structure

```
kermit_koffee/
├── app/
│   ├── __init__.py          ← app factory and extensions
│   ├── models/
│   │   ├── customer.py      ← Customer model
│   │   ├── product.py       ← Product (menu item) model
│   │   ├── order.py         ← Order model
│   │   └── order_item.py    ← OrderItem join model
│   ├── routes/
│   │   ├── auth.py          ← register and login endpoints
│   │   ├── menu.py          ← menu endpoints
│   │   ├── orders.py        ← order endpoints
│   │   └── analytics.py     ← analytics endpoints
│   ├── services/
│   │   ├── auth_service.py  ← registration and login logic
│   │   └── order_service.py ← order creation and retrieval logic
│   └── analytics/
│       └── insights.py      ← pandas analytics functions
├── simulator/
│   └── order_simulator.py   ← random order generator script
├── config.py                ← configuration (reads from .env)
├── run.py                   ← entry point
├── .env                     ← environment variables (not committed)
├── .gitignore
└── requirements.txt
```

---

## API Endpoints

### Auth

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Register a new customer |
| POST | `/auth/login` | No | Login and receive JWT token |

### Menu

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/menu` | No | Return all menu items |

### Orders

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/orders` | Yes | Place a new order |
| GET | `/orders` | Yes | Get all orders for the logged-in customer |

### Analytics

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/analytics/top-products` | Yes | Top selling products by volume |
| GET | `/analytics/revenue` | Yes | Total revenue summary |

---

## Database Schema

```
customers
  id, username, email, password_hash, created_at

products
  id, name, category, price, description

orders
  id, customer_id (FK → customers), created_at, total_amount

order_items
  id, order_id (FK → orders), product_id (FK → products), quantity, unit_price
```

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/Tee-35/Kermit-Koffee.git
cd Kermit-Koffee

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with your local config
# (see Environment Variables section below)

# 5. Create the MySQL database
mysql -u root -p
CREATE DATABASE kermit_koffee;

# 6. Run the app
python run.py
```

---

## Environment Variables

Create a `.env` file in the root directory. This file is listed in `.gitignore` and will never be committed to GitHub.

```
DB_USERNAME=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=kermit_koffee
JWT_SECRET_KEY=your_secret_key
```

---

## Author

Tyrelle Newton
GitHub: [https://github.com/Tee-35](https://github.com/Tee-35)
