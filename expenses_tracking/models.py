from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from financial_status.models import Category


User = get_user_model()
class ExpensesTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="") 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # expense amount

    def __str__(self):
        return self.title

    # Adding this because of non-nullable in db migration
    # Usage: new_expenses_tracking = ExpensesTracking.objects.create(title='Title', description='Description', user=request.user)
    def save(self, *args, **kwargs):
        if not self.user_id:
            # If user_id is not set, default to the currently logged-in user
            self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super().save(*args, **kwargs)

@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    if sender.name == 'expenses_tracking':  # Ensure this signal only runs for the expenses_tracking app
        categories = ['Bank Accounts', 'Cash', 'Other']

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
