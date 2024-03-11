from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from typing import List, Dict, Any
from django.urls import reverse

from .models import Dashboard
from financial_status.forms import FinancialStatusForm
from financial_status.models import FinancialStatus


def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    financial_status_data = user_dashboard.get_financial_status()
    last_financial_status_entries = user_dashboard.get_latest_financial_status()
    edit_urls = generate_urls(last_financial_status_entries, 'edit_financial_status')

    print(f'Edit urls: {edit_urls}')

    form = FinancialStatusForm()

    context = {
        'financial_status_data': zip(last_financial_status_entries, edit_urls),
        'form': form,
        'edit_mode': False,
    }

    return render(request, 'data_visualisation/dashboard.html', context)


def add_new_financial_status(request):
    if request.method == 'POST':
        form = FinancialStatusForm(request.POST)

        if form.is_valid():
            financial_status = form.save(commit=False)
            financial_status.user = request.user
            financial_status.save()

            print("DEBUG: add_new_financial_status")

            return(redirect('dashboard'))
    else:
        form = FinancialStatusForm()
    
    context = {'form':form}
    return(render(request, 'data_visualisation/dashboard.html', context))

def edit_financial_status(request, financial_status_id):
    print('DEBUG financial_status_id: ', financial_status_id)

    financial_status = get_object_or_404(FinancialStatus, id=financial_status_id, user=request.user)

    historical_records_for_category = financial_status.history.filter(category=financial_status.category)


    if request.method == 'POST':
        print("request.method == 'POST' for edit_financial_status")

        form = FinancialStatusForm(request.POST, instance=financial_status) 

        if form.is_valid():
            print("Form is valid for edit_financial_status")
            form.save()
            return redirect('dashboard')
        else:
            print("Form is invalid for edit_financial_status")
            print(form.errors)
    else:
        form = FinancialStatusForm()
        # print(form.instance)
    
    print("DEBUG: YOURE HERE, CHECK edit_mode")

    context = {
        'form':form,
        'edit_mode':True,
        'financial_status_id':financial_status_id,
        'historical_records_for_category': historical_records_for_category,
    }

    return render(request, 'data_visualisation/edit_financial_status.html', context)


# Utils
def generate_urls(data: List[Dict[str, Any]], url_name):
    return [reverse(url_name, args=[entry['id']]) for entry in data]
