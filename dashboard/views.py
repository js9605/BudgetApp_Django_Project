from django.shortcuts import render
from typing import List, Dict, Any
from django.urls import reverse
from datetime import datetime

from .models import Dashboard
from financial_status.forms import FinancialStatusForm
from earnings_tracking.forms import EarningsTrackingForm
from earnings_tracking.views import generate_estimated_earnings_list


def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    last_financial_status_data = user_dashboard.get_latest_financial_status()
    edit_urls = generate_urls(last_financial_status_data, 'edit_financial_status')
    financial_status_form = FinancialStatusForm()

    earning_source_form = EarningsTrackingForm()
    earning_source_data = user_dashboard.get_earning_sources()

    print("DEBUG earning_source_data: ", earning_source_data)
    print("DEBUG: USER TEST ", user_dashboard)

    estimate_future_earnings = estimate_earnings(request, earning_source_data)

    #TODO Add estimated accoubnt balance task
    amount_float = float(last_financial_status_data[0]['amount'])
    print("DEBUG amount_float: ", amount_float)
    estimated_account_balance_list = [(float(earning) + amount_float) for earning in estimate_future_earnings]

    context = {
        'estimated_account_balance_list': estimated_account_balance_list,
        'financial_status_data': zip(last_financial_status_data, edit_urls),
        'financial_status_form': financial_status_form,
        'edit_mode': False,

        'earning_source_data': earning_source_data,
        'earning_source_form': earning_source_form
    }

    return render(request, 'data_visualisation/dashboard.html', context)


# Utils
def generate_urls(data: List[Dict[str, Any]], url_name):
    return [reverse(url_name, args=[entry['id']]) for entry in data]

def estimate_earnings(request, earning_source_data):
    estimate_earnings_for_future_2_months = []
    estimated_earnings_list = generate_estimated_earnings_list(request, earning_source_data)

    for i in range(datetime.now().month+1, datetime.now().month+3):
        estimate_earnings_for_future_2_months.append(estimated_earnings_list[i])

    return estimate_earnings_for_future_2_months
