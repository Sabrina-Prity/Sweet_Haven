from django.contrib import admin
from .models import Mango, Comment
# Register your models here.

class MangoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_display = ['name', 'price', 'quantity', 'category']
    search_fields = ['name', 'category__name']
    list_filter = ['category']

    
admin.site.register(Mango, MangoAdmin)
admin.site.register(Comment)