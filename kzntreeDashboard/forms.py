# myapp/forms.py

from django import forms
from .models import UserProfile, InventoryItem, Category, BuildDashboard
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1','password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']

class ItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['sku', 'name', 'category', 'tags', 'in_stock', 'available_stock']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BuildDashboardForm(forms.ModelForm):
    class Meta:
        model = BuildDashboard
        fields = ['references', 'item_group', 'quantity', 'cost', 'linked_sale_order_group', 'creation_group_date', 'completion_group_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completion_group_date'].required = False