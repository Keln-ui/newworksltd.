import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from orders.models import Order, OrderItem
from store.models import Product
from decimal import Decimal

def run():
    print("Attempting to create Order...")
    try:
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.first()
            if not user:
                user = User.objects.create_user('testuser', 'test@example.com', 'password')
                print("Created test user")
            else:
                print(f"Using existing user: {user.username}")
        except Exception as e:
            print(f"Could not get user: {e}")
            return

        # Create a dummy order
        order = Order.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test St',
            city='Test City'
        )
        print(f"Order created: {order.id}")

        # Get a product (create one if necessary for test)
        product = Product.objects.first()
        if not product:
            print("No products found, skipping OrderItem creation.")
            return

        print(f"Using product: {product.name}")

        # Create OrderItem
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=Decimal('10.00'),
            quantity=1
        )
        print(f"OrderItem created: {item.id}")
        
        # Cleanup
        print("Cleaning up...")
        item.delete()
        order.delete()
        print("Cleanup done. Write test PASSED.")

    except Exception as e:
        print(f"Write test FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run()
