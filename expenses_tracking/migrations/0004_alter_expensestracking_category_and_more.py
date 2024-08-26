# Generated by Django 5.0.2 on 2024-08-26 16:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_tracking', '0003_expensestracking_expense_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensestracking',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='expensestracking',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expensestracking',
            name='title',
            field=models.CharField(default='Title', max_length=100),
        ),
        migrations.AlterField(
            model_name='expensestracking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
