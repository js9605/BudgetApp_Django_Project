from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# from expenses_tracking.models import ExpensesTracking #TODO
# from earnings_tracking.models import EarningsTracking #TODO
from finantial_status.models import FinantialStatus #TODO
from .forms import UserRegistrationForm


#TODO First create apps for ExpenseTracking, EarningsTracking, FinantialStatus
@login_required
def user_profile(request):
    user = request.user

    # expenses = ExpensesTracking.objects.filter(author=user).all()
    # earnings = EarningsTracking.objects.filer(author=user).all()
    finantial_status = FinantialStatus.objects.filter(user=user).all()

    context = {
        # 'expenses':expenses,
        # 'earnings':earnings,
        'finantial_status':finantial_status
    }

    return render(request, 'accounts/profile_details.html', context) #Simple version. For visual overhaul go to dashboard

def register_user(request):
    form = UserRegistrationForm() #TODO

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse('login_page'))
        
        else:
            print('Form is invalid for: register_user()')
            print(form.errors)

    context = {'form': form}
    return render(request, 'accounts/register_user.html', context)

def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        print("Log: request.method == 'POST")

        if form.is_valid():
            print("Log: form.is_valid")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                print("Log: user is not None")

                login(request, user)

                print('Here should redirect to dashboard (TODO)')
                # return redirect(reverse('dashboard')) #todo
            else:
                print("Log: user is None")

    
    context = {'form': form}
    return render(request, 'accounts/login_user.html', context)
            
def logout_user(request):
    logout(request)

    return redirect(reverse('login_page'))