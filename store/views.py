from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = None
    
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': selected_category
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def about(request):
    return render(request, 'store/about.html')

def services(request):
    return render(request, 'store/services.html')

def contacts(request):
    return render(request, 'store/contacts.html')
