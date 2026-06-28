# Kermit Koffee 🐸 — Bug Log

This document records every bug introduced, demonstrated, and fixed during Stage 2 of the build. Each entry follows the same structure: what the bug was, why it mattered, how it was found, how it was fixed, and how the fix was verified.

This stage deliberately mirrors real-world development — inheriting a codebase with issues, diagnosing them, and resolving them with clean, documented fixes.

---

## Bug 1 — Missing Input Validation on Customer Registration

### Stage
Stage 2 — Fix

### File Affected
`app/routes/auth.py`

### What Was the Bug?
The customer registration endpoint accepted any data sent to it without checking whether the required fields were present or valid. If a request was sent with empty strings for username, email, and password, the system would accept it, create a customer record with blank fields, and return a success message.

### Why Did It Matter?
- **Data integrity** — blank or invalid customer records pollute the database
- **Security** — an account with no password is a vulnerability
- **User experience** — a real app should tell the user what went wrong, not silently accept bad data
- In a production system this could allow thousands of junk accounts to be created with no way to identify real customers

### The Buggy Code
```python
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # No validation here — blank data goes straight to the database
    existing = Customer.query.filter_by(email=email).first()
    ...
```

### How It Was Demonstrated
A request was sent with empty strings for all fields:

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "", "email": "", "password": ""}'
```

**Response before fix:**
```json
{
  "message": "Welcome to Kermit Koffee, !"
}
```

The system returned a 201 Created status and saved a blank customer to the database. The welcome message showed an empty username — `"Welcome to Kermit Koffee, !"` — confirming the bad data was accepted.

### The Fix
Validation was restored and improved. The original check only verified fields were present. The fix also validates the content — minimum length for username and password, and a basic format check for email.

```python
if not username or not email or not password:
    return jsonify({'error': 'Username, email and password are required'}), 400

if len(username) < 3:
    return jsonify({'error': 'Username must be at least 3 characters'}), 400

if '@' not in email:
    return jsonify({'error': 'Invalid email address'}), 400

if len(password) < 6:
    return jsonify({'error': 'Password must be at least 6 characters'}), 400
```

### How It Was Tested After Fix
The same request was sent again:

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "", "email": "", "password": ""}'
```

**Response after fix:**
```json
{
  "error": "Username, email and password are required"
}
```

HTTP status returned: `400 Bad Request` — correct behaviour. The blank customer record that was created during testing was also removed from the database directly.

### Git Commits
- `bug: removed input validation from register endpoint`
- `fix: restore and improve input validation on register endpoint`

---

## Bug 2 — App Crash When No JSON Body Sent to Orders Endpoint

### Stage
Stage 2 — Fix

### File Affected
`app/routes/orders.py`

### What Was the Bug?
The orders endpoint used `data.get['items']` instead of `data.get('items')`. Square brackets on a method reference causes a `TypeError` crash. Additionally there was no check for whether a JSON body was sent at all.

### Why Did It Matter?
- **Availability** — a single bad request crashed the entire API for all users
- **No graceful degradation** — instead of a helpful error message the caller received an HTML error page
- In production this would cause a 500 error visible to all clients

### The Buggy Code
```python
data = request.get_json()
items = data.get['items']  # TypeError — square brackets on a method
```

### How It Was Demonstrated
A POST request was sent with an empty JSON body:

```bash
curl -X POST http://127.0.0.1:5000/orders/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer TOKEN" \
-d '{}'
```

**Result before fix:**

The app returned a full HTML error page and logged a 500 error.

### The Fix
```python
data = request.get_json()

if not data:
    return jsonify({'error': 'Request body must be JSON'}), 400

items = data.get('items', [])

if not items:
    return jsonify({'error': 'No items provided'}), 400
```

### How It Was Tested After Fix
Same request sent again:

**Response after fix:**
```json
{"error": "Request body must be JSON"}
```

HTTP status returned: `400 Bad Request` — correct behaviour. No crash.

### Git Commits
- `bug: unsafe data access causes crash when items missing from order`
- `fix: add error handling for missing JSON body and items in orders endpoint`


*More bugs to follow in Stage 3*
