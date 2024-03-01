from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Dashboard


def dashboard(request):
    user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

    finantial_status_data = user_dashboard.get_finantial_status()

    context = {
        'finantial_status_data': finantial_status_data,
    }

    return render(request, 'data_visualisation/dashboard.html', context)




"""
    @login_required
    def dashboard(request):
        user_dashboard, created = Dashboard.objects.get_or_create(user=request.user)

        # Call the method to fetch data from the expenses_tracking app
        expense_tracking_data = user_dashboard.get_expense_tracking_data()

        context = {
            'user_dashboard': user_dashboard,
            'expense_tracking_data': expense_tracking_data,
            # Include additional data as needed
        }

        return render(request, 'dashboard/dashboard.html', context)
"""