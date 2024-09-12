# Generated by Django 5.0.2 on 2024-08-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_tracking', '0006_remove_expensestracking_expense_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensestracking',
            name='expense_type',
            field=models.CharField(choices=[('single', 'Single Payment'), ('monthly', 'Monthly Recurring')], default='single', max_length=10),
        ),
    ]