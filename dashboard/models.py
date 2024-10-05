from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Max

# from expenses_tracking.models import Expenses #TODO
from financial_status.models import FinancialStatus, Category
from earnings_tracking.models import EarningsTracking

from expenses_tracking.models import ExpensesTracking



User = get_user_model()
class Dashboard(models.Model):
    """
    Keep in mind that these methods are related to fetching data from the FinancialStatus
    model, so it might make more sense to keep them within the Dashboard model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def get_financial_status(self):

        financial_statuses = FinancialStatus.objects.filter()
        financial_status_data = [
            {'id': financial_status.id,'category': financial_status.category.name, 'amount': financial_status.amount}
            for financial_status in financial_statuses
        ]

        return financial_status_data
    
    def get_latest_financial_status(self):
        latest_entries = FinancialStatus.objects.filter(user=self.user).values(
            'category'
        ).annotate(
            latest_id=Max('id')
        )

        if not latest_entries:
            return [{'id': 0, 'category': 'No Data', 'amount': 0}]
        
        latest_financial_status_data = []

        for entry in latest_entries:
            latest_entry = FinancialStatus.objects.filter(id=entry['latest_id']).first()
            if latest_entry:
                latest_financial_status_data.append({
                    'id': latest_entry.id,
                    'category': latest_entry.category.name,
                    'amount': latest_entry.amount,
                })

        return latest_financial_status_data

    def get_earning_sources(self):
        earning_sources = EarningsTracking.objects.filter()
        earning_source_data = [
            {'id': earning_source.id, 'title': earning_source.title, 'category': earning_source.category, 'amount': earning_source.amount, 'amount_type': earning_source.amount_type}
            for earning_source in earning_sources
        ]

        return earning_source_data
    
    def get_expenses_data(self):
        expenses_sources = ExpensesTracking.objects.filter()
        expenses_source_data = [
            {'id': expenses_source.id, 'title': expenses_source.title, 'category': expenses_source.category, 'amount': expenses_source.amount, 'expense_type': expenses_source.expense_type}
            for expenses_source in expenses_sources
        ]

        return expenses_source_data
