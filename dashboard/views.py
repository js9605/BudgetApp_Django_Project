from django.shortcuts import render
from typing import List, Dict, Any
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import Dashboard
from financial_status.forms import FinancialStatusForm
from earnings_tracking.forms import EarningsTrackingForm
from earnings_tracking.views import generate_estimated_earnings_list


@login_required
def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    financial_status_form = FinancialStatusForm()
    last_financial_status_data = user_dashboard.get_latest_financial_status()
    edit_urls = generate_urls(last_financial_status_data, 'edit_financial_status')

    earning_source_form = EarningsTrackingForm()
    earning_source_data = user_dashboard.get_earning_sources()

    financial_status_total_amount = sum_current_financial_status(last_financial_status_data)
    estimate_future_earnings = estimate_earnings(request, earning_source_data, financial_status_total_amount) #TODO Add expenses wyliczane z sredniej wydatkow co miesiac
    estimated_account_balance_list = [Decimal(str(earning)) + financial_status_total_amount for earning in estimate_future_earnings]

    context = {
        'estimated_account_balance_list': estimated_account_balance_list,
        'financial_status_data': zip(last_financial_status_data, edit_urls),
        'financial_status_form': financial_status_form,
        'edit_mode': False,

        'earning_source_data': earning_source_data,
        'earning_source_form': earning_source_form
    }

    return render(request, 'data_visualisation/dashboard.html', context)

def generate_urls(data: List[Dict[str, Any]], url_name):
    return [reverse(url_name, args=[entry['id']]) for entry in data]

def estimate_earnings(request, earning_source_data, financial_status_total_amount):
    estimate_earnings_for_future_2_months = []
    estimated_earnings_list = generate_estimated_earnings_list(request, earning_source_data, financial_status_total_amount) #TODO Add expenses wyliczane z sredniej wydatkow co miesiac

    current_month_number = datetime.now().month
    estimate_earnings_for_future_2_months.append(estimated_earnings_list[current_month_number - 1])
    estimate_earnings_for_future_2_months.append(estimated_earnings_list[current_month_number])

    return estimate_earnings_for_future_2_months

def sum_current_financial_status(last_financial_status_data):
    financial_status_total_amount = Decimal('0.00')
    for entry in last_financial_status_data:
        financial_status_total_amount += entry['amount']

    return financial_status_total_amount