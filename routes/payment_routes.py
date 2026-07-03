from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
import uuid

payment_bp = Blueprint('payment', __name__)

def get_mongo():
    from app import mongo
    return mongo

@payment_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('product.cart'))
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
    if request.method == 'POST':
        order = {
            'order_id': str(uuid.uuid4())[:8].upper(),
            'user_id': session.get('user_id', 'guest'),
            'user_name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'postal': request.form.get('postal'),
            'country': request.form.get('country'),
            'payment_method': request.form.get('payment_method'),
            'items': cart_items,
            'total': round(total + (0 if total >= 5000 else 499), 2),
            'status': 'confirmed',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        mongo.db.orders.insert_one(order)
        session['last_order'] = order
        session['cart'] = []
        return redirect(url_for('payment.order_confirmation'))
    return render_template('checkout.html', cart_items=detailed, total=round(total, 2), shipping=(0 if total >= 5000 else 499), grand_total=round(total + (0 if total >= 5000 else 499), 2))

@payment_bp.route('/order-confirmation')
def order_confirmation():
    order = session.get('last_order')
    if not order:
        return redirect(url_for('index'))
    return render_template('order_confirmation.html', order=order)
