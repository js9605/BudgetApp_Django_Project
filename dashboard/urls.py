from . import views
from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_new_finantial_status/', views.add_new_finantial_status, name='add_new_finantial_status')
]