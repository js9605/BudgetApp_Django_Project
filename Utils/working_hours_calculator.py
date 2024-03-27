from calendar import monthrange

from accounts.models import UserProfile
from datetime import datetime


def working_hours_per_month(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("UserProfile.DoesNotExist for calculate_working_hours_per_month")
        return None

    working_hours_per_day = user_profile.working_hours_per_day
    num_days = working_days_for_current_month()

    print(f"DEBUG: working hours: {working_hours_per_day * num_days}")

    #TODO Subtract free days, sat, sun, holidays

    return working_hours_per_day * num_days

def working_days_for_current_month():
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get the first day of the month
    first_day_of_month = datetime(current_year, current_month, 1)

    # Initialize the count of working days
    working_days = 0
    # Iterate over each day in the month
    for day in range(first_day_of_month.day, first_day_of_month.day + 31):
        current_date = datetime(current_year, current_month, day)

        # Check if the current day is a Saturday or Sunday
        if current_date.weekday() not in [5, 6]:
            working_days += 1

    return working_days




"""
USAGE:

User = get_user_model()
user = User.objects.get(username='example_user')  # Replace 'example_user' with the actual username
total_working_hours_current_month = get_working_hours_current_month(user)
print("Total working hours for the current month:", total_working_hours_current_month)

"""