from django import forms
from .models import ExpensesTracking

class ExpensesTrackingForm(forms.ModelForm):
    class Meta:
        model = ExpensesTracking
        fields = ['title', 'description', 'category', 'amount']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the description field optional
        self.fields['description'].required = False
