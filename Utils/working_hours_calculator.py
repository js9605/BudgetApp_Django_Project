from calendar import monthrange
import holidays
from django.shortcuts import redirect, get_object_or_404

from accounts.models import UserProfile
from datetime import datetime


def working_hours_per_month(request, month):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
    except UserProfile.DoesNotExist:
        print("UserProfile.DoesNotExist for calculate_working_hours_per_month")

    working_hours_given_month = generate_working_hours(month, user_profile)

    return working_hours_given_month

def generate_working_hours(month, user_profile):
    working_hours_per_day = user_profile.working_hours_per_day
    number_of_holidays_given_month = holidays_given_month(month)  

    return working_hours_per_day * (number_of_working_days(month) - number_of_holidays_given_month)

def holidays_given_month(month):
    polish_holidays = holidays.Poland()
    current_year = datetime.now().year

    free_days = 0


    current_year = datetime.now().year
    polish_holidays = holidays.Poland(years=current_year)

    for date, _ in polish_holidays.items():
        if int(month) == int(date.month):
            free_days += 1

    return free_days

def number_of_working_days(month):
    current_year = datetime.now().year
    _, num_days_in_month = monthrange(current_year, month)

    # iterate every day of the month to count only working days
    number_of_working_days = 0
    for day in range(1, num_days_in_month + 1):
        current_date = datetime(current_year, month, day)
        if current_date.weekday() not in [5, 6]:  # subtract sat/sun
            number_of_working_days += 1

    return number_of_working_days