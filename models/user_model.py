from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import random
import string

def create_user(mongo, name, email, password):
    hashed = generate_password_hash(password)
    user = {
        'name': name,
        'email': email,
        'password': hashed,
        'verified': True,   # OTP verify hone tak False rahega
        'orders': []
    }
    result = mongo.db.users.insert_one(user)
    return str(result.inserted_id)

def get_user_by_email(mongo, email):
    return mongo.db.users.find_one({'email': email})

def get_user_by_id(mongo, user_id):
    return mongo.db.users.find_one({'_id': ObjectId(user_id)})

def verify_password(user, password):
    return check_password_hash(user['password'], password)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def set_otp(mongo, email, otp):
    mongo.db.users.update_one({'email': email}, {'$set': {'otp': otp}})

def verify_otp(mongo, email, otp):
    user = get_user_by_email(mongo, email)
    if user and user.get('otp') == otp:
        mongo.db.users.update_one({'email': email}, {'$set': {'verified': True, 'otp': None}})
        return True
    return False
