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
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name','address')
    search_fields = ('name','shop_unique_id')