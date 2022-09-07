from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField,UserCreationForm

from .models import User

# to remove the redundant fields in the User Creation Form
class CustomUserCreationForm(UserCreationForm):
        model = User
        # fields = ('email', 'role')


