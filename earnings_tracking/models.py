from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_migrate

from financial_status.models import Category


User = get_user_model()
class EarningsTracking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="") 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # earnings / h

    def __str__(self):
        return self.title

    # Adding this because of non-nullable in db migration
    # Usage: new_earnings_tracking = EarningsTracking.objects.create(title='Title', description='Description', user=request.user)
    def save(self, *args, **kwargs):
        if not self.user_id:
            # If user_id is not set, default to the currently logged-in user
            self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super().save(*args, **kwargs)
    
@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    if sender.name == 'earnings_tracking':
        categories = ['Bank Accounts', 'Cash', 'Investments', 'Other']

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)