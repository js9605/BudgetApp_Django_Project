from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from .models import UserProfile
from earnings_tracking.models import EarningsTracking


User = get_user_model()
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'working_hours_per_day']

class EarningsTrackingForm(forms.ModelForm):
    class Meta:
        model = EarningsTracking
        fields = ['title', 'description', 'category', 'amount', 'amount_type']