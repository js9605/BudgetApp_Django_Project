from django.urls import path

from . import views


urlpatterns = [
    # path('user_profile/', views.user_profile, name='user_profile'), #TODO
    path('signup/', views.register_user, name='signup_page'),
    path('login/', views.login_user, name='login_page'),
    path('logout/', views.logout_user, name='logout_page')
    
    # Handle password reset here
]