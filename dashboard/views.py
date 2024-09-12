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
    monthly_expenses_data = user_dashboard.get_monthly_expenses_data()

    # Estimations, including expenses
    estimated_future_earnings = estimate_earnings(request, earning_source_data)
    estimated_future_earnings = apply_expenses(estimated_future_earnings, monthly_expenses_data)
    estimated_account_balance_list = estimate_financial_statuses(estimated_future_earnings, financial_status_total_amount)

    # Pass everything to context
    context = {
        'estimated_account_balance_list': estimated_account_balance_list,
        'financial_status_data': zip(last_financial_status_data, edit_urls),
        'financial_status_form': financial_status_form,
        'edit_mode': False,

        'earning_source_data': earning_source_data,
        'earning_source_form': earning_source_form,

        'expenses_data': monthly_expenses_data,
        'expenses_form': expenses_form,
    }

    return render(request, 'data_visualisation/dashboard.html', context)

def generate_urls(data: List[Dict[str, Any]], url_name):
    return [reverse(url_name, args=[entry['id']]) for entry in data]

def estimate_earnings(request, earning_source_data):
    estimate_earnings_for_future_2_months = []
    estimated_earnings_list = generate_estimated_earnings_list(request, earning_source_data)

    current_month_number = datetime.now().month
    estimate_earnings_for_future_2_months.append(estimated_earnings_list[current_month_number - 1])
    estimate_earnings_for_future_2_months.append(estimated_earnings_list[current_month_number])

    return estimate_earnings_for_future_2_months

def sum_current_financial_status(last_financial_status_data):
    financial_status_total_amount = Decimal('0.00')
    for entry in last_financial_status_data:
        financial_status_total_amount += entry['amount']

    return financial_status_total_amount

def apply_expenses(estimated_future_earnings, expenses_data):
    total_expenses = 0

    for expense in expenses_data:
        if expense['expense_type'] == "monthly": #TODO Im getting too much money in account balance because im not adding expenses because they have type = single
            total_expenses += expense['amount']

    estimated_account_balance_list = [earning - total_expenses for earning in estimated_future_earnings] # *2 for current and future month estimation xD

    return estimated_account_balance_list

def estimate_financial_statuses(estimated_future_earnings, financial_status_total_amount):
    estimated_account_balance_list = []
    for earning in estimated_future_earnings:
        account_balance_single_month = Decimal(str(earning)) + financial_status_total_amount
        estimated_account_balance_list.append(account_balance_single_month)
        financial_status_total_amount = account_balance_single_month

    return estimated_account_balance_list