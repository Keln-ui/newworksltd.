import os
import django
import sys
from django.test import Client

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from store.models import Product

def verify_currency():
    # 1. Setup Data
    product, _ = Product.objects.get_or_create(
        name='Currency Test Product',
        price=1000,
        defaults={'description': 'Test currency symbol'}
    )

    c = Client()

    # 2. Check Product List
    print("\n--- Testing Product List ---")
    response = c.get('/')
    if b'KES 1000' in response.content:
        print("SUCCESS: Product List shows KES.")
    else:
        print("FAILURE: Product List does NOT show KES.")

    # 3. Check Product Detail
    print("\n--- Testing Product Detail ---")
    response = c.get(product.get_absolute_url())
    if b'KES 1000' in response.content:
        print("SUCCESS: Product Detail shows KES.")
    else:
        print("FAILURE: Product Detail does NOT show KES.")

    # 4. Check Cart (Add item first)
    print("\n--- Testing Cart ---")
    c.post(f'/cart/add/{product.id}/', {'quantity': 1, 'update': False})
    response = c.get('/cart/')
    if b'KES 1000' in response.content:
        print("SUCCESS: Cart Detail shows KES.")
    else:
        print("FAILURE: Cart Detail does NOT show KES.")

if __name__ == '__main__':
    verify_currency()
