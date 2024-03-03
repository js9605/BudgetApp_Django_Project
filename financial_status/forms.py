from django import forms

from .models import FinancialStatus



class FinancialStatusForm(forms.ModelForm):
    class Meta:
        model = FinancialStatus
        fields = [
            'amount',
            'category',
            # 'date' #TODO should i add this?
        ]