from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from datetime import datetime

from earnings_tracking.forms import EarningsTrackingForm
from earnings_tracking.models import EarningsTracking
from Utils.working_hours_calculator import working_hours_per_month


def add_new_earning_source(request):
    # TODO Add Celery worker to update financial_status every month (like employee payment)
    if request.method == 'POST':
        form = EarningsTrackingForm(request.POST)

        if form.is_valid():
            earning_source = form.save(commit=False)
            earning_source.user = request.user

            earning_source.save()

            return redirect('dashboard')
        else:
            print("DEBUG: Form invalid for add_new_earning_source()")

    else:
        form = EarningsTrackingForm()

    context = {'form': form}
    return(render(request, 'data_visualisation/dashboard.html'), context)

def add_new_earning(request):
    """
    TODO
    Should add possibility to add externall earning by hand
        - Not periodic
        - One entry to update *Account Balance*
    """
    pass

def delete_earning_source(request, pk):
    earning_source = get_object_or_404(EarningsTracking, pk=pk)

    if request.method == 'POST':
        earning_source.delete()
        return redirect('dashboard')
    
    return redirect('dashboard')

def generate_estimated_earnings_list(request,  earning_source_data):
    list_of_earnings_per_month = []

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    amounts = [entry['amount']  for entry in earning_source_data]
    category = [entry['category']  for entry in earning_source_data]
    
    for month in months:

        print("DEBUG")
        print(earning_source_data)
        # print(amounts)
        # print(working_hours_per_month(request, month))
        
        # for amount in amounts: #TODO divide it to calculate per category!
        #     month_sum =+ amount * working_hours_per_month(request, month)

        # list_of_earnings_per_month.append(month_sum)

    # return list_of_earnings_per_month
