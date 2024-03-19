from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

from financial_status.models import Category


User = get_user_model()
class EarningsTracking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField() 
    
    # Category to which add money
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # amount of earnings / h used to calculate earnings at the end of the month
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.title

