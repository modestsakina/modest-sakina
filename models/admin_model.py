from werkzeug.security import generate_password_hash, check_password_hash

# ═══════════════════════════════════════════════════════
#  SIRF AAPKA ADMIN ACCOUNT — Change karo agar chahiye
# ═══════════════════════════════════════════════════════
ADMIN_USERNAME = "sakina_admin"          # Aapka username
ADMIN_PASSWORD = "Sakina@2024#Secure"    # Aapka password (strong)
ADMIN_NAME     = "Modest Sakina Owner"   # Display name

def create_default_admin(mongo):
    """Har baar check karta hai - agar admin nahi hai toh banata hai"""
    existing = mongo.db.admins.find_one({'username': ADMIN_USERNAME})
    if not existing:
        # Purane default admin delete karo
        mongo.db.admins.delete_many({})
        mongo.db.admins.insert_one({
            'username': ADMIN_USERNAME,
            'password': generate_password_hash(ADMIN_PASSWORD),
            'name': ADMIN_NAME,
            'is_owner': True
        })
        print(f"✅ Admin account ready — username: {ADMIN_USERNAME}")
    else:
        # Password update karo agar match nahi karta (protection)
        if not check_password_hash(existing['password'], ADMIN_PASSWORD):
            mongo.db.admins.update_one(
                {'username': ADMIN_USERNAME},
                {'$set': {'password': generate_password_hash(ADMIN_PASSWORD)}}
            )

def get_admin(mongo, username):
    return mongo.db.admins.find_one({'username': username})

def verify_admin_password(admin, password):
    return check_password_hash(admin['password'], password)
