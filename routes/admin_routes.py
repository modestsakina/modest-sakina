from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from models.admin_model import get_admin, verify_admin_password
from bson import ObjectId
import os
import uuid
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def get_mongo():
    from app import mongo
    return mongo

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Admin login required.', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@admin_required
def dashboard():
    mongo = get_mongo()
    total_products = mongo.db.products.count_documents({})
    total_orders = mongo.db.orders.count_documents({})
    total_users = mongo.db.users.count_documents({})
    total_messages = mongo.db.messages.count_documents({})
    recent_orders = list(mongo.db.orders.find().sort('_id', -1).limit(5))
    for o in recent_orders:
        o['_id'] = str(o['_id'])
    return render_template('admin/dashboard.html',
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
        total_messages=total_messages,
        recent_orders=recent_orders
    )

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Brute-force protection
        attempts = session.get('admin_attempts', 0)
        if attempts >= 5:
            flash('Too many failed attempts. Please restart the server.', 'danger')
            return render_template('admin/login.html')
        
        mongo = get_mongo()
        admin = get_admin(mongo, username)
        if admin and verify_admin_password(admin, password):
            session['admin_logged_in'] = True
            session['admin_name'] = admin['name']
            session.pop('admin_attempts', None)
            flash('Welcome back, ' + admin['name'] + '!', 'success')
            return redirect(url_for('admin.dashboard'))
        
        session['admin_attempts'] = attempts + 1
        remaining = 5 - (attempts + 1)
        flash(f'Invalid credentials. {remaining} attempts remaining.', 'danger')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_name', None)
    flash('Logged out from admin panel.', 'info')
    return redirect(url_for('admin.login'))

# ── PRODUCTS ──────────────────────────────────────────────
@admin_bp.route('/products')
@admin_required
def products():
    mongo = get_mongo()
    products = list(mongo.db.products.find().sort('name', 1))
    for p in products:
        p['_id'] = str(p['_id'])
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    mongo = get_mongo()
    categories = [
        'Premium Hijab', 'Chiffon Hijab', 'Silk Hijab', 'Cotton Hijab',
        'Jersey Hijab', 'Sports Hijab', 'Instant Hijab', 'Bridal Hijab',
        'Embroidered Hijab', 'Luxury Hijab', 'Everyday Hijab', 'Printed Hijab',
        'Satin Hijab', 'Kids Hijab', 'Abaya & Hijab Sets'
    ]
    if request.method == 'POST':
        image_url = ''
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            file = request.files['image_file']
            if allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = str(uuid.uuid4()) + '.' + ext
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = '/static/uploads/' + filename
        if not image_url:
            image_url = request.form.get('image_url', '').strip()
        if not image_url:
            image_url = 'https://images.unsplash.com/photo-1594938298603-c8148c4b4d51?w=500'

        product = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': float(request.form.get('price', 0)),
            'description': request.form.get('description'),
            'image': image_url,
            'stock': int(request.form.get('stock', 0)),
            'featured': 'featured' in request.form
        }
        mongo.db.products.insert_one(product)
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=None, categories=categories, action='Add')

@admin_bp.route('/products/edit/<product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    mongo = get_mongo()
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.products'))
    product['_id'] = str(product['_id'])
    categories = [
        'Premium Hijab', 'Chiffon Hijab', 'Silk Hijab', 'Cotton Hijab',
        'Jersey Hijab', 'Sports Hijab', 'Instant Hijab', 'Bridal Hijab',
        'Embroidered Hijab', 'Luxury Hijab', 'Everyday Hijab', 'Printed Hijab',
        'Satin Hijab', 'Kids Hijab', 'Abaya & Hijab Sets'
    ]
    if request.method == 'POST':
        image_url = product['image']
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            file = request.files['image_file']
            if allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = str(uuid.uuid4()) + '.' + ext
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = '/static/uploads/' + filename
        elif request.form.get('image_url', '').strip():
            image_url = request.form.get('image_url').strip()

        updated = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': float(request.form.get('price', 0)),
            'description': request.form.get('description'),
            'image': image_url,
            'stock': int(request.form.get('stock', 0)),
            'featured': 'featured' in request.form
        }
        mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': updated})
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=product, categories=categories, action='Edit')

@admin_bp.route('/products/delete/<product_id>')
@admin_required
def delete_product(product_id):
    mongo = get_mongo()
    mongo.db.products.delete_one({'_id': ObjectId(product_id)})
    flash('Product deleted.', 'info')
    return redirect(url_for('admin.products'))

@admin_bp.route('/products/toggle-featured/<product_id>')
@admin_required
def toggle_featured(product_id):
    mongo = get_mongo()
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if product:
        mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'featured': not product.get('featured', False)}})
    return redirect(url_for('admin.products'))

# ── ORDERS ──────────────────────────────────────────────
@admin_bp.route('/orders')
@admin_required
def orders():
    mongo = get_mongo()
    orders = list(mongo.db.orders.find().sort('_id', -1))
    for o in orders:
        o['_id'] = str(o['_id'])
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/update-status/<order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    mongo = get_mongo()
    status = request.form.get('status')
    mongo.db.orders.update_one({'_id': ObjectId(order_id)}, {'$set': {'status': status}})
    flash('Order status updated.', 'success')
    return redirect(url_for('admin.orders'))

# ── MESSAGES ──────────────────────────────────────────────
@admin_bp.route('/messages')
@admin_required
def messages():
    mongo = get_mongo()
    msgs = list(mongo.db.messages.find().sort('_id', -1))
    for m in msgs:
        m['_id'] = str(m['_id'])
    return render_template('admin/messages.html', messages=msgs)

@admin_bp.route('/messages/delete/<msg_id>')
@admin_required
def delete_message(msg_id):
    mongo = get_mongo()
    mongo.db.messages.delete_one({'_id': ObjectId(msg_id)})
    flash('Message deleted.', 'info')
    return redirect(url_for('admin.messages'))

# ── USERS ──────────────────────────────────────────────
@admin_bp.route('/users')
@admin_required
def users():
    mongo = get_mongo()
    users = list(mongo.db.users.find({}, {'password': 0}).sort('_id', -1))
    for u in users:
        u['_id'] = str(u['_id'])
    return render_template('admin/users.html', users=users)
