from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name',)
    # This makes choosing products inside a supplier profile clean and user-friendly
    filter_horizontal = ('products',)