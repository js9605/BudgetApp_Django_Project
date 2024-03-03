from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Dashboard
from financial_status.forms import FinancialStatusForm
from financial_status.models import FinancialStatus


def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    financial_status_data = user_dashboard.get_financial_status()

    form = FinancialStatusForm()

    context = {
        'financial_status_data': financial_status_data,
        'form': form,
    }

    return render(request, 'data_visualisation/dashboard.html', context)


def add_new_financial_status(request):
    if request.method == 'POST':
        form = FinancialStatusForm(request.POST)

        if form.is_valid():
            financial_status = form.save(commit=False)
            financial_status.user = request.user
            financial_status.save()

            return(redirect('dashboard'))
    else:
        form = FinancialStatusForm()
    
    context = {'form':form}
    return(render(request, 'data_visualisation/dashboard.html', context))

def edit_financial_status(request, financial_status_id):
    pass
