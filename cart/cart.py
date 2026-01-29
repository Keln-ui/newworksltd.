from decimal import Decimal
from django.conf import settings
from store.models import Product
from .models import Cart as CartModel, CartItem

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            
            # If user is authenticated, try to load cart from database
            if self.user.is_authenticated:
                try:
                    db_cart = CartModel.objects.get(user=self.user)
                    for item in db_cart.items.all():
                        cart[str(item.product.id)] = {'quantity': item.quantity, 'price': str(item.product.sell_price)}
                    self.session[settings.CART_SESSION_ID] = cart
                except CartModel.DoesNotExist:
                    pass
                    
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.sell_price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # Filter out non-numeric IDs that might cause issues
        valid_product_ids = [pid for pid in product_ids if pid.isdigit()]
        
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=valid_product_ids)
        cart = {}
        
        for product in products:
            cart_key = str(product.id)
            if cart_key in self.cart:
                # Create a new dict for each item to avoid modifying session data
                cart[cart_key] = {
                    'product': product,
                    'quantity': self.cart[cart_key]['quantity'],
                    'price': Decimal(self.cart[cart_key]['price']),
                }
                cart[cart_key]['total_price'] = cart[cart_key]['price'] * cart[cart_key]['quantity']

        # Remove items with invalid product IDs from the session cart
        invalid_keys = [key for key in self.cart.keys() if not key.isdigit() or key not in cart]
        if invalid_keys:
            for item_key in invalid_keys:
                del self.cart[item_key]
            self.save()

        for item in cart.values():
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.cart = {}
        
        # remove cart from database if authenticated
        if self.user.is_authenticated:
            try:
                db_cart = CartModel.objects.get(user=self.user)
                db_cart.items.all().delete()
            except CartModel.DoesNotExist:
                pass
                
        self.session.modified = True

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
        
        # sync to database if authenticated
        if self.user.is_authenticated:
            db_cart, created = CartModel.objects.get_or_create(user=self.user)
            # Use a more efficient update: remove all and Add all (simple but effective for small carts)
            # Or update efficiently. For simplicity:
            db_cart.items.all().delete()
            for product_id, item_data in self.cart.items():
                product = Product.objects.get(id=product_id)
                CartItem.objects.create(
                    cart=db_cart,
                    product=product,
                    quantity=item_data['quantity']
                )
