from . import views
from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('add_new_financial_status/', views.add_new_financial_status, name='add_new_financial_status'),
    path('edit_financial_status/<int:financial_status_id>/', views.edit_financial_status, name='edit_financial_status'),

    # TODO
    # path('add_new_earning_source/', views.add_new_earning_source, name='add_new_earning_source'),
    # path('add_new_earning/', views.add_new_earning, name='add_new_earning')
]