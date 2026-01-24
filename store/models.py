from django.db import models

from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def sell_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
