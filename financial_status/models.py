from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    
User = get_user_model()
class FinancialStatus(models.Model):

    """
    historical_records = financial_status.history.all() # Access
    Retrieve historical records for the specific category
    historical_records_for_category = financial_status.history.filter(category=category)
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # (e.g., bank accounts, cash)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_created_in_dashboard = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username}'s Financial Status"


@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    if sender.name == 'financial_status':
        categories = ['Bank Accounts', 'Cash', 'Other']

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
