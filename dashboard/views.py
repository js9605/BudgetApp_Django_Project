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
from expenses_tracking.forms import ExpensesTrackingForm



@login_required
def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    # Financial status data and form
    financial_status_form = FinancialStatusForm()
    last_financial_status_data = user_dashboard.get_latest_financial_status()
    edit_urls = generate_urls(last_financial_status_data, 'edit_financial_status')
    financial_status_total_amount = sum_current_financial_status(last_financial_status_data)

    # Earning source data and form
    earning_source_form = EarningsTrackingForm()
    earning_source_data = user_dashboard.get_earning_sources()

    # Expenses data and form
    expenses_form = ExpensesTrackingForm()
    expenses_data = user_dashboard.get_expenses_sources() #TODO It should be clear that its monthly expenses!

    # Estimations, including expenses
    estimate_future_earnings = estimate_earnings(request, earning_source_data, financial_status_total_amount)
    estimate_future_earnings = apply_expenses(estimate_future_earnings, expenses_data)

    estimated_account_balance_list = [Decimal(str(earning)) + financial_status_total_amount for earning in estimate_future_earnings]

    # estimated_account_balance_list = [
    #     Decimal(str(earning)) + financial_status_total_amount - sum(expense.amount for expense in expenses_data)
    #     for earning in estimate_future_earnings
    # ]

    # Pass everything to context
    context = {
        'estimated_account_balance_list': estimated_account_balance_list,
        'financial_status_data': zip(last_financial_status_data, edit_urls),
        'financial_status_form': financial_status_form,
        'edit_mode': False,

        'earning_source_data': earning_source_data,
        'earning_source_form': earning_source_form,

        'expenses_data': expenses_data,
        'expenses_form': expenses_form,
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

def apply_expenses(estimate_future_earnings, expenses_data):
    total_expenses = sum(expense['amount'] for expense in expenses_data)

    estimated_account_balance_list = [
        earning - total_expenses for earning in estimate_future_earnings
    ]

    return estimated_account_balance_list
