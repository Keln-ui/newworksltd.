from django.contrib import admin
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'total_cost', 'order_detail']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]
    
    def order_detail(self, obj):
        url = reverse('admin_order_detail', args=[obj.id])
        return format_html('<a href="{}">View Detail</a>', url)
