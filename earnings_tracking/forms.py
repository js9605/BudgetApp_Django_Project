from django import forms
from .models import EarningsTracking

class EarningsTrackingForm(forms.ModelForm):
    class Meta:
        model = EarningsTracking
        fields = ['title', 'description', 'category', 'amount', 'amount_type']  # Ensure 'amount_type' is included

    labels = {
        'amount': 'Earnings per hour or month',  # Adjust label as needed
        'amount_type': 'Amount Type',  # Label for amount_type
    }

    amount_type = forms.ChoiceField(
        choices=[('hour', 'Per Hour'), ('month', 'Per Month')],
        widget=forms.RadioSelect,
        label="Amount Type"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False