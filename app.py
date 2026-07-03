from flask import Flask, render_template, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_mail import Mail
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.payment_routes import payment_bp
from routes.admin_routes import admin_bp
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'modestsakina_secret_key_2024'
app.permanent_session_lifetime = timedelta(days=7)

import os

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'modestsakina@gmail.com'
app.config['MAIL_PASSWORD'] = 'axqv iqtl eprh pmwc'
app.config['MAIL_DEFAULT_SENDER'] = 'modestsakina@gmail.com'

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

mongo = PyMongo(app)
mail = Mail(app)

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    from models.product_model import get_featured_products, get_categories
    products = get_featured_products(mongo)
    categories = get_categories(mongo)
    return render_template('index.html', products=products, categories=categories)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    from flask import request, flash
    if request.method == 'POST':
        msg = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message')
        }
        mongo.db.messages.insert_one(msg)
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.context_processor
def inject_cart_count():
    cart = session.get('cart', [])
    return dict(cart_count=len(cart))

if __name__ == '__main__':
    with app.app_context():
        from models.product_model import seed_products
        from models.admin_model import create_default_admin
        seed_products(mongo)
        create_default_admin(mongo)
    app.run(debug=True)
