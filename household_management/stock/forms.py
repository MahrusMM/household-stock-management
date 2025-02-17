from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# ✅ Define Role Choices Here
ROLE_CHOICES = [
    ('parent', 'Parent'),
    ('child', 'Child'),
]

# ✅ Register Form (User Signup)
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

# ✅ Login Form (Authentication)
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'quantity', 'category', 'price','low_stock_threshold']  # Make sure these match your model
