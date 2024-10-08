# Generated by Django 5.0.2 on 2024-08-26 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_tracking', '0004_alter_expensestracking_category_and_more'),
        ('financial_status', '0005_alter_financialstatus_timestamp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensestracking',
            name='category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='financial_status.category'),
        ),
        migrations.AlterField(
            model_name='expensestracking',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='expensestracking',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='expensestracking',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
