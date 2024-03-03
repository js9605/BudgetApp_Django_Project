from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# from expenses_tracking.models import Expenses #TODO
from financial_status.models import FinancialStatus


User = get_user_model()
class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_financial_status(self):

        financial_statuses = FinancialStatus.objects.filter()
        financial_status_data = [
            {'category': financial_status.category.name, 'amount': financial_status.amount}
            for financial_status in financial_statuses
        ]

        return financial_status_data
    
    # def get_expense_tracking_data(self):

    #     # Fetch and format data from the expenses_tracking app
    #     expenses = Expenses.objects.filter(user=self.user)
    #     expense_data = '\n'.join([f"{expense.category}: ${expense.amount}" for expense in expenses])
    #     return expense_data


