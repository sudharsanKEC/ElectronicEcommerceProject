from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(District)

# admin.site.register(WebAppAdmin)


@admin.register(WebAppAdmin)
class WebAppAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'district', 'unique_id', 'created_at')
    list_filter = ('district', 'created_at')
    search_fields = ('name', 'email', 'unique_id')

@admin.register(Shop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ('shop_name','address')
    list_filter = ('district',)
    search_fields = ('name','shop_unique_id')

@admin.register(ShopAdmin)
class ShopAdminModelAdmin(admin.ModelAdmin):
    list_display = ('admin_id','admin_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','shop','product_unique_id')