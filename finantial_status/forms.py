from django import forms

from .models import FinantialStatus



class FinancialStatusForm(forms.ModelForm):
    class Meta:
        model = FinantialStatus
        fields = [
            'amount',
            'category',
            # 'date' #TODO should i add this?
        ]