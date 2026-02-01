import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from store.models import Category, Product
from decimal import Decimal

# Create Adapters category
category, created = Category.objects.get_or_create(
    slug='adapters',
    defaults={
        'name': 'Fiber Optic Adapters',
        'description': 'High-quality fiber optic adapters for various connector types. Essential components for fiber optic connections and patch panels.'
    }
)

if created:
    print(f"[+] Created category: {category.name}")
else:
    print(f"[+] Category already exists: {category.name}")

# Adapter products data
adapters_data = [
    {
        'name': 'SC/UPC to SC/UPC Simplex Adapter',
        'description': '''Single-mode SC/UPC simplex adapter. Features:
• Ceramic sleeve for low insertion loss
• Simplex (single port) design
• SC to SC connection
• UPC polish for better performance
• Low insertion loss (<0.3dB)
• High return loss (>50dB)
• Suitable for telecom and datacom applications''',
        'price': Decimal('150.00'),
        'discount_price': Decimal('120.00'),
        'stock': 200
    },
    {
        'name': 'SC/APC to SC/APC Simplex Adapter',
        'description': '''Single-mode SC/APC simplex adapter. Features:
• Angled Physical Contact (APC) for minimal back reflection
• Green color coding
• Ceramic sleeve
• Low insertion loss (<0.3dB)
• Very high return loss (>60dB)
• Ideal for CATV and high-performance networks
• Prevents signal reflection''',
        'price': Decimal('180.00'),
        'discount_price': Decimal('150.00'),
        'stock': 180
    },
    {
        'name': 'LC/UPC to LC/UPC Duplex Adapter',
        'description': '''Compact LC duplex adapter. Features:
• Small form factor design
• Duplex (dual port) configuration
• Ceramic sleeve
• Blue housing (single-mode)
• Low insertion loss (<0.3dB)
• High density applications
• Perfect for data centers and high-density panels''',
        'price': Decimal('200.00'),
        'discount_price': Decimal('170.00'),
        'stock': 250
    },
    {
        'name': 'LC/APC to LC/APC Duplex Adapter',
        'description': '''LC duplex adapter with APC polish. Features:
• Angled connector for superior performance
• Green color coding
• Duplex configuration
• Ultra-low back reflection
• High return loss (>60dB)
• Ideal for FTTH and PON networks
• Space-saving design''',
        'price': Decimal('220.00'),
        'discount_price': Decimal('190.00'),
        'stock': 220
    },
    {
        'name': 'FC/UPC to FC/UPC Simplex Adapter',
        'description': '''Threaded FC simplex adapter. Features:
• Screw-type connection
• Ceramic sleeve
• High stability and reliability
• Low insertion loss (<0.3dB)
• Suitable for test equipment
• Industrial applications
• Vibration resistant''',
        'price': Decimal('250.00'),
        'discount_price': Decimal('220.00'),
        'stock': 150
    },
    {
        'name': 'ST to ST Simplex Adapter',
        'description': '''Bayonet-style ST adapter. Features:
• Twist-lock mechanism
• Multimode and single-mode compatible
• Ceramic or bronze sleeve options
• Reliable connection
• Easy installation
• Legacy system support
• Cost-effective solution''',
        'price': Decimal('180.00'),
        'discount_price': Decimal('150.00'),
        'stock': 120
    },
    {
        'name': 'SC to LC Hybrid Adapter',
        'description': '''Hybrid adapter for different connector types. Features:
• SC on one side, LC on other
• Enables connection between different systems
• Single-mode compatible
• Ceramic sleeve
• Low insertion loss
• Versatile solution
• Ideal for system upgrades''',
        'price': Decimal('280.00'),
        'discount_price': Decimal('250.00'),
        'stock': 100
    },
    {
        'name': 'SC to FC Hybrid Adapter',
        'description': '''SC to FC hybrid adapter. Features:
• Connects SC and FC connectors
• Single-mode and multimode versions
• High-quality ceramic sleeve
• Low insertion loss
• Reliable performance
• Equipment compatibility
• Professional grade''',
        'price': Decimal('300.00'),
        'discount_price': Decimal('270.00'),
        'stock': 90
    },
    {
        'name': 'MPO/MTP to MPO/MTP Adapter',
        'description': '''High-density MPO/MTP adapter. Features:
• 12 or 24 fiber support
• Key-up to key-down configuration
• Ultra-high density
• Low insertion loss
• Ideal for data centers
• 40G/100G applications
• Precision alignment''',
        'price': Decimal('1200.00'),
        'discount_price': Decimal('1050.00'),
        'stock': 50
    },
    {
        'name': 'E2000/APC to E2000/APC Adapter',
        'description': '''E2000 adapter with shutter protection. Features:
• Built-in shutter mechanism
• APC polish
• Dust protection
• High return loss (>60dB)
• Push-pull design
• Ideal for clean environments
• Premium quality''',
        'price': Decimal('450.00'),
        'discount_price': Decimal('400.00'),
        'stock': 80
    },
    {
        'name': 'SC Quad Adapter Panel',
        'description': '''Four-port SC adapter panel. Features:
• Quad (4-port) configuration
• Flange mount design
• Metal housing
• Suitable for patch panels
• Easy installation
• Professional appearance
• Durable construction''',
        'price': Decimal('600.00'),
        'discount_price': Decimal('550.00'),
        'stock': 60
    },
    {
        'name': 'LC Quad Adapter Panel',
        'description': '''High-density LC quad adapter. Features:
• 4 duplex LC ports (8 fibers)
• Compact design
• Metal housing
• Flange mount
• High port density
• Data center grade
• Easy cable management''',
        'price': Decimal('650.00'),
        'discount_price': Decimal('600.00'),
        'stock': 70
    }
]

# Create products
created_count = 0
updated_count = 0

for adapter_data in adapters_data:
    product, created = Product.objects.update_or_create(
        name=adapter_data['name'],
        defaults={
            'category': category,
            'description': adapter_data['description'],
            'price': adapter_data['price'],
            'discount_price': adapter_data['discount_price'],
            'stock': adapter_data['stock']
        }
    )
    
    if created:
        created_count += 1
        print(f"[+] Created: {product.name} - KES {product.price}")
    else:
        updated_count += 1
        print(f"[+] Updated: {product.name} - KES {product.price}")

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Category: {category.name}")
print(f"  Products created: {created_count}")
print(f"  Products updated: {updated_count}")
print(f"  Total adapter products: {Product.objects.filter(category=category).count()}")
print(f"{'='*60}")
print("\nNote: Please add images for these products through the Django admin interface.")
print("Recommended image names: sc-upc-adapter.jpg, lc-duplex-adapter.jpg, etc.")
