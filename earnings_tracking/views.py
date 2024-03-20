from django.shortcuts import redirect, render

from earnings_tracking.forms import EarningsTrackingForm


def add_new_earning_source(request):
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
    pass