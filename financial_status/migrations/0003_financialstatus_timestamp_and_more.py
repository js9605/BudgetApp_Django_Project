# Generated by Django 5.0.2 on 2024-03-11 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_status', '0002_historicalfinancialstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialstatus',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='historicalfinancialstatus',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]