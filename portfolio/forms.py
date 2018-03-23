from django import forms
from .models import Volunteer, Inventory

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('vol_number', 'lname', 'fname','vol_dob', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone','vol_notes')


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            'donor', 'item_code', 'item_name', 'item_quantity', 'acquired_date',)

