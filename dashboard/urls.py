from . import views
from django.urls import path

from financial_status.views import add_new_financial_status, edit_financial_status
from earnings_tracking.views import add_new_earning_source, delete_earning_source
from expenses_tracking.views import add_new_expense, delete_expense

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # Financial Status URLs
    path('add_new_financial_status/', add_new_financial_status, name='add_new_financial_status'),
    path('edit_financial_status/<int:financial_status_id>/', edit_financial_status, name='edit_financial_status'),

    # Earnings Tracking URLs
    path('add_new_earning_source/', add_new_earning_source, name='add_new_earning_source'),
    path('delete_earning_source/<int:pk>/', delete_earning_source, name='delete_earning_source'),

    # Expenses Tracking URLs
    path('add_new_expense/', add_new_expense, name='add_new_expense'),
    path('delete_expense/<int:pk>/', delete_expense, name='delete_expense'),
]
