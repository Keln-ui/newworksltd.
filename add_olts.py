import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from store.models import Category, Product
from decimal import Decimal

# Create OLTs category
category, created = Category.objects.get_or_create(
    slug='olts',
    defaults={
        'name': 'OLTs',
        'description': 'Optical Line Terminals (OLTs) for fiber optic networks. High-performance equipment for GPON, EPON, and XG-PON networks.'
    }
)

if created:
    print(f"[+] Created category: {category.name}")
else:
    print(f"[+] Category already exists: {category.name}")

# OLT products data
olts_data = [
    {
        'name': 'Huawei MA5800-X7 OLT',
        'description': '''High-density OLT supporting up to 16 service slots. Features:
• Supports GPON, 10G GPON, and XG-PON
• Up to 1024 ONUs per slot
• Advanced QoS and traffic management
• Redundant power supply and control boards
• Hot-swappable modules
• Ideal for large-scale FTTH deployments''',
        'price': Decimal('450000.00'),
        'discount_price': Decimal('420000.00'),
        'stock': 5
    },
    {
        'name': 'ZTE C320 OLT',
        'description': '''Compact and cost-effective OLT solution. Features:
• Supports GPON and EPON
• Up to 8 PON ports per card
• 1U chassis design
• Easy management via web interface
• Supports up to 1024 ONUs
• Perfect for small to medium deployments''',
        'price': Decimal('280000.00'),
        'discount_price': Decimal('265000.00'),
        'stock': 8
    },
    {
        'name': 'Huawei MA5608T Mini OLT',
        'description': '''Compact mini OLT for small deployments. Features:
• 8 GPON ports
• Desktop or rack-mountable
• Supports up to 512 ONUs
• Low power consumption
• Easy configuration and management
• Ideal for MDU and small business deployments''',
        'price': Decimal('85000.00'),
        'discount_price': Decimal('78000.00'),
        'stock': 12
    },
    {
        'name': 'ZTE C300 OLT',
        'description': '''Enterprise-grade OLT with advanced features. Features:
• Modular design with up to 10 slots
• Supports GPON, EPON, and 10G PON
• High-density port configuration
• Advanced security features
• Comprehensive network management
• Suitable for large enterprise networks''',
        'price': Decimal('380000.00'),
        'discount_price': Decimal('355000.00'),
        'stock': 6
    },
    {
        'name': 'Huawei MA5800-X15 OLT',
        'description': '''Ultra-high capacity OLT for carrier networks. Features:
• Up to 32 service slots
• Supports all PON technologies
• Carrier-grade reliability
• Advanced traffic engineering
• Distributed architecture
• Designed for metro and core networks''',
        'price': Decimal('850000.00'),
        'discount_price': Decimal('795000.00'),
        'stock': 3
    },
    {
        'name': 'Fiberhome AN5516-06 OLT',
        'description': '''Versatile OLT with excellent performance. Features:
• 6 PON slots
• Supports GPON and EPON
• Flexible configuration options
• Built-in OAM capabilities
• Energy-efficient design
• Great for medium-sized networks''',
        'price': Decimal('195000.00'),
        'discount_price': Decimal('180000.00'),
        'stock': 10
    },
    {
        'name': 'Nokia 7360 ISAM FX OLT',
        'description': '''Premium OLT with cutting-edge technology. Features:
• Supports XGS-PON and NG-PON2
• Ultra-low latency
• Advanced automation features
• Carrier-grade performance
• Scalable architecture
• Perfect for next-generation networks''',
        'price': Decimal('920000.00'),
        'discount_price': Decimal('875000.00'),
        'stock': 2
    },
    {
        'name': 'Huawei MA5801-GP08 Mini OLT',
        'description': '''Compact 8-port GPON OLT. Features:
• 8 GPON ports
• Fanless design
• Low power consumption
• Simple web management
• Supports up to 512 ONUs
• Ideal for small deployments and testing''',
        'price': Decimal('65000.00'),
        'discount_price': Decimal('58000.00'),
        'stock': 15
    }
]

# Create products
created_count = 0
updated_count = 0

for olt_data in olts_data:
    product, created = Product.objects.update_or_create(
        name=olt_data['name'],
        defaults={
            'category': category,
            'description': olt_data['description'],
            'price': olt_data['price'],
            'discount_price': olt_data['discount_price'],
            'stock': olt_data['stock']
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
print(f"  Total OLT products: {Product.objects.filter(category=category).count()}")
print(f"{'='*60}")
print("\nNote: Please add images for these products through the Django admin interface.")
print("Recommended image names: huawei-ma5800-x7.jpg, zte-c320.jpg, etc.")
