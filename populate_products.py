import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from store.models import Product

def populate():
    products = [
        {
            'name': 'Smartphone X Pro',
            'description': 'Latest generative AI features, 256GB storage, and a stunning 6.8-inch display.',
            'price': 999.00,
            'stock': 50
        },
        {
            'name': 'Wireless Noise-Cancelling Headphones',
            'description': 'Immersive sound with industry-leading noise cancellation and 30-hour battery life.',
            'price': 299.99,
            'stock': 100
        },
        {
            'name': 'Ergonomic Office Chair',
            'description': 'Breathable mesh back, adjustable lumbar support, and comfortable seat cushion for long hours.',
            'price': 199.50,
            'stock': 25
        },
        {
            'name': '4K Ultra HD Generic Monitor',
            'description': '27-inch IPS panel with HDR10 for crystal clear visuals and vibrant colors.',
            'price': 349.00,
            'stock': 30
        },
        {
            'name': 'Mechanical Gaming Keyboard',
            'description': 'RGB backlighting, tactile switches, and durable aluminum frame.',
            'price': 89.99,
            'stock': 75
        },
        {
            'name': 'Stainless Steel Water Bottle',
            'description': 'Double-wall vacuum insulation keeps drinks cold for 24 hours or hot for 12.',
            'price': 24.95,
            'stock': 200
        },
        {
            'name': 'Classic Cotton T-Shirt',
            'description': 'Soft, breathable 100% cotton tee available in multiple sizes.',
            'price': 15.00,
            'stock': 500
        },
        {
            'name': 'Smart Watch Series 5',
            'description': 'Fitness tracking, heart rate monitor, and seamless connectivity with your phone.',
            'price': 199.00,
            'stock': 60
        }
    ]

    print("Populating database with products...")
    for p_data in products:
        product, created = Product.objects.get_or_create(
            name=p_data['name'],
            defaults={
                'description': p_data['description'],
                'price': Decimal(str(p_data['price'])),
                'stock': p_data['stock']
            }
        )
        if created:
            print(f"Created: {product.name}")
        else:
            print(f"Exists: {product.name}")

    print("Done!")

if __name__ == '__main__':
    populate()
