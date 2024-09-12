from django import forms
from .models import EarningsTracking

class EarningsTrackingForm(forms.ModelForm):
    labels = {
        'amount': 'Earnings per hour or month',
        'amount_type': 'Amount Type',
    }

    amount_type = forms.ChoiceField(
        choices=[('hour', 'per Hour'), ('month', 'per Month')],
        widget=forms.RadioSelect,
        label="Amount Type"
    )
    class Meta:
        model = EarningsTracking
        fields = ['title', 'description', 'category', 'amount', 'amount_type']  # Ensure 'amount_type' is included
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False