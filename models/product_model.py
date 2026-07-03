from bson import ObjectId

PRODUCTS = [
    {'name': 'Pearl Shimmer Premium Hijab', 'category': 'Premium Hijab', 'price': 3999, 'description': 'Luxurious premium fabric with pearl shimmer finish. Perfect for special occasions.', 'image': 'https://images.unsplash.com/photo-1594938298603-c8148c4b4d51?w=500', 'featured': True, 'stock': 50},
    {'name': 'Ivory Cloud Chiffon Hijab', 'category': 'Chiffon Hijab', 'price': 1999, 'description': 'Lightweight chiffon with a dreamy drape. Breathable and elegant.', 'image': 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=500', 'featured': True, 'stock': 80},
    {'name': 'Rose Gold Silk Hijab', 'category': 'Silk Hijab', 'price': 5499, 'description': 'Pure silk in a stunning rose gold tone. The ultimate in luxury modesty wear.', 'image': 'https://images.unsplash.com/photo-1617019114583-affb34d1b3cd?w=500', 'featured': True, 'stock': 30},
    {'name': 'Soft Blush Cotton Hijab', 'category': 'Cotton Hijab', 'price': 1599, 'description': 'Organic cotton blend, perfect for everyday comfort. Hypoallergenic and soft.', 'image': 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=500', 'featured': True, 'stock': 120},
    {'name': 'Stretch Jersey Hijab', 'category': 'Jersey Hijab', 'price': 1399, 'description': 'Flexible jersey material that stays in place all day. Great for active wear.', 'image': 'https://images.unsplash.com/photo-1594938298603-c8148c4b4d51?w=500', 'featured': False, 'stock': 100},
    {'name': 'ActiveFit Sports Hijab', 'category': 'Sports Hijab', 'price': 2399, 'description': 'Moisture-wicking performance fabric. Designed for sport and active lifestyle.', 'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500', 'featured': True, 'stock': 60},
    {'name': 'QuickWrap Instant Hijab', 'category': 'Instant Hijab', 'price': 1699, 'description': 'No-pin design, ready in seconds. Ideal for busy mornings.', 'image': 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=500', 'featured': False, 'stock': 90},
    {'name': 'Ivory Lace Bridal Hijab', 'category': 'Bridal Hijab', 'price': 7499, 'description': 'Delicate lace trim bridal hijab for your special day. Includes crystal pins.', 'image': 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=500', 'featured': True, 'stock': 20},
    {'name': 'Gold Thread Embroidered Hijab', 'category': 'Embroidered Hijab', 'price': 4599, 'description': 'Intricate gold thread embroidery on soft fabric. A statement piece.', 'image': 'https://images.unsplash.com/photo-1617019114583-affb34d1b3cd?w=500', 'featured': True, 'stock': 35},
    {'name': 'Cashmere Luxury Hijab', 'category': 'Luxury Hijab', 'price': 9999, 'description': 'Pure cashmere blend for unmatched softness and warmth. A true luxury item.', 'image': 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=500', 'featured': True, 'stock': 15},
    {'name': 'Neutral Everyday Hijab', 'category': 'Everyday Hijab', 'price': 1249, 'description': 'Your perfect everyday companion. Available in 20+ colours.', 'image': 'https://images.unsplash.com/photo-1594938298603-c8148c4b4d51?w=500', 'featured': False, 'stock': 200},
    {'name': 'Floral Printed Hijab', 'category': 'Printed Hijab', 'price': 2099, 'description': 'Beautiful floral print on lightweight fabric. Vibrant and stylish.', 'image': 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=500', 'featured': False, 'stock': 75},
    {'name': 'Champagne Satin Hijab', 'category': 'Satin Hijab', 'price': 2749, 'description': 'Glossy satin finish in champagne. Elegant for evenings and events.', 'image': 'https://images.unsplash.com/photo-1617019114583-affb34d1b3cd?w=500', 'featured': True, 'stock': 45},
    {'name': 'Pastel Kids Hijab Set', 'category': 'Kids Hijab', 'price': 1099, 'description': 'Soft pastel hijab set designed for girls. Comfortable and easy to wear.', 'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500', 'featured': False, 'stock': 80},
    {'name': 'Majestic Abaya & Hijab Set', 'category': 'Abaya & Hijab Sets', 'price': 12499, 'description': 'Matching abaya and hijab set. Flowing fabric with elegant tailoring.', 'image': 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=500', 'featured': True, 'stock': 25},
    {'name': 'Dusty Rose Premium Hijab', 'category': 'Premium Hijab', 'price': 4099, 'description': 'Dusty rose premium hijab with satin border. Sophisticated and refined.', 'image': 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=500', 'featured': False, 'stock': 40},
    {'name': 'Mint Chiffon Hijab', 'category': 'Chiffon Hijab', 'price': 1849, 'description': 'Fresh mint chiffon for a light, airy look. Perfect for summer.', 'image': 'https://images.unsplash.com/photo-1594938298603-c8148c4b4d51?w=500', 'featured': False, 'stock': 65},
    {'name': 'Midnight Navy Silk Hijab', 'category': 'Silk Hijab', 'price': 5749, 'description': 'Deep navy pure silk. Timeless elegance for any occasion.', 'image': 'https://images.unsplash.com/photo-1617019114583-affb34d1b3cd?w=500', 'featured': False, 'stock': 28},
    {'name': 'Geometric Printed Hijab', 'category': 'Printed Hijab', 'price': 2249, 'description': 'Modern geometric print in earthy tones. Contemporary modest fashion.', 'image': 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=500', 'featured': False, 'stock': 55},
    {'name': 'Silver Embroidered Hijab', 'category': 'Embroidered Hijab', 'price': 4899, 'description': 'Silver thread embroidery on ivory chiffon. Stunning for formal events.', 'image': 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=500', 'featured': False, 'stock': 30},
]

def seed_products(mongo):
    if mongo.db.products.count_documents({}) == 0:
        mongo.db.products.insert_many(PRODUCTS)

def get_all_products(mongo, category=None, search=None):
    query = {}
    if category:
        query['category'] = category
    if search:
        query['$or'] = [
            {'name': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}},
            {'category': {'$regex': search, '$options': 'i'}}
        ]
    products = list(mongo.db.products.find(query))
    for p in products:
        p['_id'] = str(p['_id'])
    return products

def get_featured_products(mongo):
    products = list(mongo.db.products.find({'featured': True}).limit(8))
    for p in products:
        p['_id'] = str(p['_id'])
    return products

def get_product_by_id(mongo, product_id):
    try:
        product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])
        return product
    except:
        return None

def get_categories(mongo):
    return mongo.db.products.distinct('category')
