from django import forms

from .models import FinancialStatus
from financial_status.models import Category


class FinancialStatusForm(forms.ModelForm):
    class Meta:
        model = FinancialStatus
        fields = [
            'amount',
            'category',
        ]