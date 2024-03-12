from django import forms

from .models import FinancialStatus
from financial_status.models import Category



class FinancialStatusForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(FinancialStatusForm, self).__init__(*args, **kwargs)
    #     self.fields['is_created_in_dashboard'].initial = False
    
    class Meta:
        model = FinancialStatus
        fields = [
            'amount',
            'category',
            # 'is_created_in_dashboard',
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['is_created_in_dashboard'].initial = False