from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Dashboard
from finantial_status.forms import FinancialStatusForm # TODO


def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    finantial_status_data = user_dashboard.get_finantial_status()

    form = FinancialStatusForm()

    """
    The context containing both 'finantial_status_data' and 'form' is 
    necessary because it allows you to display the existing data and provide
    a form for users to add new entries on the same dashboard page. 
    The existing data ('finantial_status_data') is displayed, and the form ('form') 
    is used to gather new data from the user.
    """

    context = {
        'finantial_status_data': finantial_status_data,
        'form': form,
    }

    return render(request, 'data_visualisation/dashboard.html', context)


def add_new_finantial_status(request):
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


def edit_finantial_status(request):
    pass