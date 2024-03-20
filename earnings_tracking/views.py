from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from earnings_tracking.forms import EarningsTrackingForm
from earnings_tracking.models import EarningsTracking


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