from django.shortcuts import render
from typing import List, Dict, Any
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import plotly.express as px
import plotly.io as pio

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
    expenses_data = user_dashboard.get_expenses_data()

    #Apply single earning and expense here
    last_financial_status_data = update_financial_status_with_single_earning(last_financial_status_data, earning_source_data)
    last_financial_status_data = update_financial_status_with_single_expense(last_financial_status_data, expenses_data)

    # Estimations, including expenses
    estimated_future_earnings = estimate_earnings(request, earning_source_data, 5)
    estimated_future_earnings = apply_expenses_for_estimated_acc_balance(estimated_future_earnings, expenses_data)
    estimated_account_balance_list = estimate_financial_statuses(estimated_future_earnings, financial_status_total_amount)

    # Plots
    graph = generate_plot_for_estimated_acc_balance(estimated_account_balance_list)

    context = {
        'estimated_account_balance_list': estimated_account_balance_list,
        'financial_status_data': zip(last_financial_status_data, edit_urls),
        'financial_status_form': financial_status_form,
        'edit_mode': False, #TODO Why that? 

        'earning_source_data': earning_source_data,
        'earning_source_form': earning_source_form,

        'expenses_data': expenses_data,
        'expenses_form': expenses_form,

        'graph': graph,
    }

    return render(request, 'data_visualisation/dashboard.html', context)

def generate_urls(data: List[Dict[str, Any]], url_name):
    return [reverse(url_name, args=[entry['id']]) for entry in data]

def estimate_earnings(request, earning_source_data, how_many_months):
    estimate_earnings_for_future_2_months = []
    estimated_earnings_list = generate_estimated_earnings_list(request, earning_source_data)

    current_month_number = datetime.now().month

    for month in range(how_many_months):
        month_idx = current_month_number + month - 1

        if month_idx > 11:
            break

        estimate_earnings_for_future_2_months.append(estimated_earnings_list[month_idx])

    return estimate_earnings_for_future_2_months

def sum_current_financial_status(last_financial_status_data):
    financial_status_total_amount = Decimal('0.00')
    for entry in last_financial_status_data:
        financial_status_total_amount += entry['amount']

    return financial_status_total_amount

def update_financial_status_with_single_earning(last_financial_status_data, earning_source_data):
    try:
        for earning in earning_source_data:
            if earning['amount_type'] == 'single':
                for i in range(len(last_financial_status_data)):
                    if last_financial_status_data[i]['category'] == earning['category'].name:
                        last_financial_status_data[i]['amount'] += earning['amount']
                       
        return last_financial_status_data
    
    except Exception as e:
        print(f"Exception occured in update_financial_status_with_single_earning: {e}")
        return last_financial_status_data

def update_financial_status_with_single_expense(last_financial_status_data, expenses_source_data):
    try:
        for expense in expenses_source_data:
            if expense['expense_type'] == 'single':
                for i in range(len(last_financial_status_data)):
                    if last_financial_status_data[i]['category'] == expense['category'].name:
                        last_financial_status_data[i]['amount'] -= expense['amount']

        return last_financial_status_data

    except Exception as e:
        print(f"Exception occured in update_financial_status_with_single_expense: {e}")
        return last_financial_status_data

def apply_expenses_for_estimated_acc_balance(estimated_future_earnings, expenses_data):
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

def generate_plot_for_estimated_acc_balance(estimated_account_balance_list):
    """
    KEEP IT SIMPLE AT START!

    Plot with whole year in months vs plot with future 6 months
        If creating whole year plots what should be placed in past months? 
    After creating plot get rid of Estimation for future months in Acccount Balance board

    """

    i = 0
    current_month_number = datetime.now().month
    months = []

    for estimated_blance in estimated_account_balance_list:
        months.append(current_month_number + i)
        i = i + 1

    fig = px.line(x=months, y=estimated_account_balance_list, title='Estimated Account Balance Over Time')
    graph = pio.to_html(fig, full_html=False)

    return graph