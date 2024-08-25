from django import forms
from .models import ExpensesTracking

class ExpensesTrackingForm(forms.ModelForm):
    class Meta:
        model = ExpensesTracking
        fields = ['title', 'description', 'category', 'amount']
