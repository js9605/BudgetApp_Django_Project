from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from datetime import datetime

from earnings_tracking.forms import EarningsTrackingForm
from earnings_tracking.models import EarningsTracking
from Utils.working_hours_calculator import working_hours_per_month


def add_new_earning_source(request):
    if request.method == 'POST':
        form = EarningsTrackingForm(request.POST)

        if form.is_valid():
            earning_source = form.save(commit=False)
            earning_source.user = request.user

            earning_source.save()

            return redirect('dashboard')
        else:
            print("DEBUG: Form errors:", form.errors)
            print("DEBUG: Form invalid for add_new_earning_source()")

    else:
        form = EarningsTrackingForm()

    context = {'form': form}
    return(render(request, 'data_visualisation/dashboard.html'), context)

def delete_earning_source(request, pk):
    earning_source = get_object_or_404(EarningsTracking, pk=pk)

    print("DEBUG delete_earning_source/earning_source: ", earning_source)

    if request.method == 'POST' and EarningsTracking.objects.count() > 1:
        earning_source.delete()
        return redirect('dashboard')
    elif EarningsTracking.objects.count() == 1:
        earning_source.title = "No earnings"
        earning_source.amount = 0
        earning_source.save()
    
    return redirect('dashboard')

def generate_estimated_earnings_list(request,  earning_source_data):
    print("\n---generate_estimated_earnings_list---\n")
    list_of_earnings_per_month = []

    earning_source_data_months = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_sum_per_hour = 0
    month_sum_per_month = 0

    if earning_source_data:
        for month in earning_source_data_months:
            for entry in earning_source_data:

                if entry['amount_type'] == "hour":
                    working_hours_given_month = working_hours_per_month(request, month)
                    month_sum_per_hour = entry['amount'] * working_hours_given_month
                elif entry['amount_type'] == "month": 
                    month_sum_per_month = entry['amount']

            # if month != 1:
                # list_of_earnings_per_month.append(month_sum_per_hour + month_sum_per_month + financial_status_total_amount + list_of_earnings_per_month[month - 2])
            # else:
            list_of_earnings_per_month.append(month_sum_per_hour + month_sum_per_month)

        return list_of_earnings_per_month #TODO Add expenses wyliczane z sredniej wydatkow co miesiac

    else:
        print("LogError: User earning_source_data is empty")
        return redirect('dashboard')