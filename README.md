# 🧕 Modest Sakina — Hijab Store

## 🚀 Setup & Run

### Requirements Install
```bash
pip install -r requirements.txt
```

### MongoDB Start karo
```bash
mongod
```

### App Chalao
```bash
python app.py
```
Site: http://localhost:5000

---

## 🔐 Admin Panel

**URL:** http://localhost:5000/admin

| Field    | Value                  |
|----------|------------------------|
| Username | `sakina_admin`         |
| Password | `Sakina@2024#Secure`   |

> ⚠️ Password change karna hai toh `models/admin_model.py` mein `ADMIN_PASSWORD` update karo aur server restart karo.

---

## 💰 Currency
Sab prices **Indian Rupees (₹)** mein hain.
Free shipping **₹5000** se upar ke orders pe.

---

## 📁 Structure
```
modest_sakina/
├── app.py                  # Main Flask app
├── models/
│   ├── admin_model.py      # Admin account
│   ├── product_model.py    # Products
│   └── user_model.py       # Users
├── routes/
│   ├── admin_routes.py     # Admin panel
│   ├── auth_routes.py      # Login/Register
│   ├── payment_routes.py   # Checkout
│   └── product_routes.py   # Cart & Products
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── uploads/            # Product images
└── templates/
    ├── admin/              # Admin templates
    └── *.html              # Store templates
```
