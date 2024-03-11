from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Max

# from expenses_tracking.models import Expenses #TODO
from financial_status.models import FinancialStatus, Category


User = get_user_model()

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Should i change this to extracting only latest entry for each category? 
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

        latest_financial_status_data = []

        for entry in latest_entries:
            latest_entry = FinancialStatus.objects.filter(id=entry['latest_id']).first()
            if latest_entry:
                latest_financial_status_data.append({
                    'id': latest_entry.id,
                    'category': latest_entry.category.name,
                    'amount': latest_entry.amount,
                })

        print(f"DEBUG: latest_financial_status_data inside DashboardModel: {latest_financial_status_data}")

        return latest_financial_status_data
    
    # def get_expense_tracking_data(self):

    #     # Fetch and format data from the expenses_tracking app
    #     expenses = Expenses.objects.filter(user=self.user)
    #     expense_data = '\n'.join([f"{expense.category}: ${expense.amount}" for expense in expenses])
    #     return expense_data


