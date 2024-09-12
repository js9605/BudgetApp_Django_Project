from django import forms
from .models import ExpensesTracking

class ExpensesTrackingForm(forms.ModelForm):
    EXPENSE_TYPE_CHOICES = [
        ('single', 'Single Payment'),
        ('monthly', 'Monthly Recurring'),
    ]
    
    expense_type = forms.ChoiceField(
        choices=EXPENSE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='single'
    )

    class Meta:
        model = ExpensesTracking
        fields = ['title', 'description', 'category', 'amount', 'expense_type']  # Include 'expense_type' field
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the description field optional
        self.fields['description'].required = False
