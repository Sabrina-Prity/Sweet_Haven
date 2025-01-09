from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import AddToCart, Order, Cart

class AddToCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'mango', 'quantity')
    search_fields = ('user__username', 'mango__name')  
    list_filter = ('user', 'mango')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'buying_status', 'purchased_at')  
    search_fields = ('user__username', 'product__name')  
    list_filter = ('buying_status', 'purchased_at')

    
admin.site.register(AddToCart, AddToCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
