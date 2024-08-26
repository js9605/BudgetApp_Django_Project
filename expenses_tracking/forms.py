from django import forms
from .models import ExpensesTracking

class ExpensesTrackingForm(forms.ModelForm):
    # Assuming you have an 'expense_type' field in your model that distinguishes between single and monthly expenses
    # EXPENSE_TYPE_CHOICES = [
    #     ('single', 'Single Payment'),
    #     ('monthly', 'Monthly Recurring'),
    # ]
    # expense_type = forms.ChoiceField(choices=EXPENSE_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = ExpensesTracking
        fields = ['title', 'description', 'category', 'amount']  # Include 'expense_type' field
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the description field optional
        self.fields['description'].required = False