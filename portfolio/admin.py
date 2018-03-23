from django.contrib import admin
from .models import Volunteer, Inventory

class VolunteerList(admin.ModelAdmin):
    list_display = ('vol_number', 'fname', 'city', 'cell_phone')
    list_filter = ('vol_number', 'fname', 'city')
    search_fields = ('vol_number', 'fname')
    ordering = ['vol_number']

class InventoryList(admin.ModelAdmin):
    list_display = ('donor', 'item_code', 'item_name', 'item_quantity')
    list_filter = ('donor', 'item_name')
    search_fields = ('donor', 'item_name')
    ordering = ['item_code']

admin.site.register(Volunteer, VolunteerList)
admin.site.register(Inventory, InventoryList)
