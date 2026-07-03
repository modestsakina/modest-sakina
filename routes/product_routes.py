from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash

product_bp = Blueprint('product', __name__)

def get_mongo():
    from app import mongo
    return mongo

@product_bp.route('/products')
def products():
    from models.product_model import get_all_products, get_categories
    mongo = get_mongo()
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    all_products = get_all_products(mongo, category=category if category else None, search=search if search else None)
    categories = get_categories(mongo)
    return render_template('product.html', products=all_products, categories=categories, selected_category=category, search=search)

@product_bp.route('/product/<product_id>')
def product_detail(product_id):
    from models.product_model import get_product_by_id, get_all_products
    mongo = get_mongo()
    product = get_product_by_id(mongo, product_id)
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('product.products'))
    related = get_all_products(mongo, category=product['category'])
    related = [p for p in related if p['_id'] != product_id][:4]
    return render_template('product_detail.html', product=product, related=related)

@product_bp.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    mongo = get_mongo()
    from models.product_model import get_product_by_id
    detailed = []
    total = 0
    for item in cart_items:
        p = get_product_by_id(mongo, item['product_id'])
        if p:
            p['quantity'] = item['quantity']
            p['subtotal'] = round(p['price'] * item['quantity'], 2)
            total += p['subtotal']
            detailed.append(p)
    return render_template('cart.html', cart_items=detailed, total=round(total, 2))

@product_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        flash('Invalid product.', 'danger')
        return redirect(request.referrer or url_for('product.products'))
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            session['cart'] = cart
            session.modified = True   # ← BUG FIX
            flash('Cart updated!', 'success')
            return redirect(request.referrer or url_for('product.cart'))
    cart.append({'product_id': product_id, 'quantity': quantity})
    session['cart'] = cart
    session.modified = True           # ← BUG FIX
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('product.cart'))

@product_bp.route('/remove-from-cart/<product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart
    session.modified = True
    flash('Item removed from cart.', 'info')
    return redirect(url_for('product.cart'))

@product_bp.route('/update-cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            if quantity <= 0:
                cart.remove(item)
            else:
                item['quantity'] = quantity
            break
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('product.cart'))
