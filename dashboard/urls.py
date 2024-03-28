from . import views
from django.urls import path

from financial_status.views import add_new_financial_status, edit_financial_status
from earnings_tracking.views import add_new_earning_source, add_new_earning, delete_earning_source

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    #TODO Separate urls later to according apps
    path('add_new_financial_status/', add_new_financial_status, name='add_new_financial_status'),
    path('edit_financial_status/<int:financial_status_id>/', edit_financial_status, name='edit_financial_status'),

    path('add_new_earning_source/', add_new_earning_source, name='add_new_earning_source'),
    # path('add_single_earning/', add_new_earning, name='add_new_earning') #TODO
    path('delete_earning_source/<int:pk>/', delete_earning_source, name='delete_earning_source'),
]