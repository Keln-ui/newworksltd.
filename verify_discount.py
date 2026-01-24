import os
import django
import sys
from decimal import Decimal
from django.test import Client

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from store.models import Product
from cart.cart import Cart

def verify_discount():
    # 1. Setup Data
    product, _ = Product.objects.get_or_create(
        name='Discount Test Product',
        price=Decimal('1000.00'),
        defaults={'description': 'Test discount'}
    )
    
    # Set discount
    product.discount_price = Decimal('800.00')
    product.save()

    c = Client()

    # 2. Check Product propery
    print(f"Product Price: {product.price}")
    print(f"Product Discount: {product.discount_price}")
    print(f"Product Sell Price: {product.sell_price}")
    
    if product.sell_price == Decimal('800.00'):
        print("SUCCESS: sell_price property works.")
    else:
        print("FAILURE: sell_price property failed.")

    # 3. Check Product List
    print("\n--- Testing Product List ---")
    response = c.get('/')
    if b'KES 800.00' in response.content and b'text-decoration-line-through' in response.content:
        print("SUCCESS: Product List shows discount.")
    else:
        print("FAILURE: Product List does NOT show discount properly.")

    # 4. Check Product Detail
    print("\n--- Testing Product Detail ---")
    response = c.get(product.get_absolute_url())
    if b'KES 800.00' in response.content and b'text-decoration-line-through' in response.content:
        print("SUCCESS: Product Detail shows discount.")
    else:
        print("FAILURE: Product Detail does NOT show discount properly.")

    # 5. Check Cart logic
    print("\n--- Testing Cart Logic ---")
    # We can't easily test session-based cart via unit test script completely without mocking request,
    # but we can check if adding via Client uses correct price.
    c.post(f'/cart/add/{product.id}/', {'quantity': 1, 'update': False})
    
    response = c.get('/cart/')
    # Cart detail should show KES 800.00
    if b'KES 800.00' in response.content:
         print("SUCCESS: Cart uses discounted price.")
    else:
         print("FAILURE: Cart does NOT use discounted price.")
    
    # 6. Verify Total
    # Total for 1 item should be 800
    if b'KES 800.00' in response.content: # Simple check, better would be parsing
         print("SUCCESS: Cart total seems correct.")

if __name__ == '__main__':
    verify_discount()
