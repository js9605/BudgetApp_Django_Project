from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# from expenses_tracking.models import Expenses #TODO
from finantial_status.models import FinantialStatus


User = get_user_model()
class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_finantial_status(self):

        finantial_statuses = FinantialStatus.objects.filter() #TODO add user in FinantialStatus models
        finantial_status_data = [
            {'category': finantial_status.category.name, 'amount': finantial_status.amount}
            for finantial_status in finantial_statuses
        ]

        return finantial_status_data
    
    # def get_expense_tracking_data(self):

    #     # Fetch and format data from the expenses_tracking app
    #     expenses = Expenses.objects.filter(user=self.user)
    #     expense_data = '\n'.join([f"{expense.category}: ${expense.amount}" for expense in expenses])
    #     return expense_data


