from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import create_user, get_user_by_email, verify_password

auth_bp = Blueprint('auth', __name__)

def get_mongo():
    from app import mongo
    return mongo


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        mongo = get_mongo()
        user = get_user_by_email(mongo, email)

        if user and verify_password(user, password):
            session.permanent = True
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']

            flash('Welcome back, ' + user['name'] + '!', 'success')
            return redirect(url_for('index'))

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not name or not email or not password:
            flash('Please fill all fields.', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        mongo = get_mongo()

        if get_user_by_email(mongo, email):
            flash('Email already registered. Please login.', 'danger')
            return render_template('register.html')

        create_user(mongo, name, email, password)

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('auth.login'))

    mongo = get_mongo()

    from models.user_model import get_user_by_id

    user = get_user_by_id(mongo, session['user_id'])

    orders = list(
        mongo.db.orders.find(
            {'user_id': session['user_id']}
        ).sort('_id', -1)
    )

    for order in orders:
        order['_id'] = str(order['_id'])

    return render_template(
        'dashboard.html',
        user=user,
        orders=orders
    )