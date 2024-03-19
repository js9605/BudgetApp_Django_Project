from . import views
from django.urls import path

from financial_status.views import add_new_financial_status, edit_financial_status

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('add_new_financial_status/', add_new_financial_status, name='add_new_financial_status'),
    path('edit_financial_status/<int:financial_status_id>/', edit_financial_status, name='edit_financial_status'),

    # TODO
    # path('add_new_earning_source/', views.add_new_earning_source, name='add_new_earning_source'),
    # path('add_new_earning/', views.add_new_earning, name='add_new_earning')
]