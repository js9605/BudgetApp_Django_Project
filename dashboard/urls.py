from . import views
from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_new_financial_status/', views.add_new_financial_status, name='add_new_financial_status'),
    # path('edit_financial_status/<int:financial_status_id>/', views.edit_financial_status, name='edit_financial_status')
    path('edit_financial_status/<int:financial_status_id>/', views.edit_financial_status, name='edit_financial_status')


]

"""
TODO
add:
- edit their current financial status (Make separate view for editing every 
    financial_status displayed in dashboard)
- delete currenct financial status (keep history of changes somwhere)
"""
