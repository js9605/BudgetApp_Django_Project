from django.shortcuts import render
from typing import List, Dict, Any
from django.urls import reverse

from .models import Dashboard
from financial_status.forms import FinancialStatusForm
from earnings_tracking.forms import EarningsTrackingForm


def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    last_financial_status_data = user_dashboard.get_latest_financial_status()
    edit_urls = generate_urls(last_financial_status_data, 'edit_financial_status')
    financial_status_form = FinancialStatusForm()

    earning_source_form = EarningsTrackingForm()
    earning_source_data = user_dashboard.get_earning_sources()

    context = {
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

