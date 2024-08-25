from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

# from expenses_tracking.models import ExpensesTracking #TODO
from financial_status.models import FinancialStatus
from .forms import UserRegistrationForm, EditUserProfileForm, EarningsTrackingForm
from .models import UserProfile
from .forms import EditUserProfileForm
from Utils.working_hours_calculator import working_hours_per_month
from earnings_tracking.models import EarningsTracking


@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Initialize forms
    profile_form = EditUserProfileForm(instance=profile)
    earnings_form = EarningsTrackingForm()

    financial_status = FinancialStatus.objects.filter(user=user).all()
    working_hours = working_hours_per_month(request, datetime.now().month)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = EditUserProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('user_profile')

        elif 'save_earnings' in request.POST:
            earnings_form = EarningsTrackingForm(request.POST)
            if earnings_form.is_valid():
                earnings_tracking = earnings_form.save(commit=False)
                earnings_tracking.user = user
                earnings_tracking.save()
                return redirect('user_profile')

    context = {
        'working_hours': working_hours,
        'profile_form': profile_form,
        'earnings_form': earnings_form,
        'financial_status': financial_status
    }

    return render(request, 'accounts/profile_details.html', context)

def register_user(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()  # Save the user
            UserProfile.objects.create(user=user) # Create UserProfile for the newly registered user

            return redirect(reverse('login_page'))
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print(f"Form errors(register_user): {form.errors}")

    context = {'form': form}
    return render(request, 'accounts/register_user.html', context)

def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            print("Log: form.is_valid")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                print("Log: user is not None")

                login(request, user)

                return redirect(reverse('dashboard'))
            else:
                print("Log: user is None")

    
    context = {'form': form}
    return render(request, 'accounts/login_user.html', context)
            
def logout_user(request):
    logout(request)

    return redirect(reverse('login_page'))