from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import (
    create_user, get_user_by_email, verify_password,
    generate_otp, set_otp, verify_otp
)
from flask_mail import Message

auth_bp = Blueprint('auth', __name__)

def get_mongo():
    from app import mongo
    return mongo

def get_mail():
    from app import mail
    return mail

def send_otp_email(email, otp):
    mail = get_mail()

    print("MAIL_SERVER:", mail.server)
    print("MAIL_PORT:", mail.port)
    print("MAIL_USERNAME:", mail.username)

    msg = Message(
        "Your Modest Sakina Verification Code",
        recipients=[email]
    )
    msg.body = f"Your OTP is: {otp}"

    try:
        mail.send(msg)
        print("EMAIL SENT SUCCESSFULLY")
    except Exception as e:
        print("MAIL ERROR:", repr(e))
        raise

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
            if not user.get('verified'):
                otp = generate_otp()
                set_otp(mongo, email, otp)
                send_otp_email(email, otp)
                flash('Please verify your email first. A new OTP has been sent.', 'warning')
                return redirect(url_for('auth.verify_otp_page', email=email))
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
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

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

        # User create karo (unverified state me)
        create_user(mongo, name, email, password)

        # OTP generate karke email bhejo
        otp = generate_otp()
        set_otp(mongo, email, otp)
        send_otp_email(email, otp)

        flash('OTP sent to your email. Please verify to continue.', 'info')
        return redirect(url_for('auth.verify_otp_page', email=email))

    return render_template('register.html')

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp_page():
    email = request.args.get('email') or request.form.get('email')
    if not email:
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        mongo = get_mongo()

        if verify_otp(mongo, email, otp):
            user = get_user_by_email(mongo, email)
            session.permanent = True
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            flash('Account verified! Welcome, ' + user['name'] + '! 🎉', 'success')
            return redirect(url_for('index'))

        flash('Invalid OTP. Please try again.', 'danger')
        return redirect(url_for('auth.verify_otp_page', email=email))

    return render_template('verify_otp.html', email=email)

@auth_bp.route('/resend-otp')
def resend_otp():
    email = request.args.get('email')
    if not email:
        return redirect(url_for('auth.register'))

    mongo = get_mongo()
    user = get_user_by_email(mongo, email)
    if not user:
        flash('No account found. Please register.', 'danger')
        return redirect(url_for('auth.register'))

    otp = generate_otp()
    set_otp(mongo, email, otp)
    send_otp_email(email, otp)
    flash('A new OTP has been sent to your email.', 'info')
    return redirect(url_for('auth.verify_otp_page', email=email))

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
    orders = list(mongo.db.orders.find({'user_id': session['user_id']}).sort('_id', -1))
    for o in orders:
        o['_id'] = str(o['_id'])
    return render_template('dashboard.html', user=user, orders=orders)
