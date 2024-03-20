from django import forms

from .models import EarningsTracking


class EarningsTrackingForm(forms.ModelForm):
    class Meta:
        model = EarningsTracking
        fields = [
            'title',
            'category',
            'amount'
        ]
        labels = {
            'amount': 'Monthly Earnings'
        }