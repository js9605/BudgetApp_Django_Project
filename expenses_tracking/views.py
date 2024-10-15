from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ExpensesTrackingForm
from .models import ExpensesTracking
from financial_status.models import FinancialStatus, Category


def add_expense(request):
    if request.method == 'POST':
        form = ExpensesTrackingForm(request.POST)

        if form.is_valid():
            expense_amount = form.cleaned_data['amount']
            expense_amount_type = form.cleaned_data['expense_type']
            expense_category = form.cleaned_data['category']


            expense = form.save(commit=False)
            expense.user = request.user

            expense.save()

            update_financial_status_with_single_excpense(request.user, expense_amount, expense_amount_type, expense_category)

            return redirect('dashboard')
        else:
            print(form.errors)

    else:
        form = ExpensesTrackingForm()

    context = {'form': form}
    return render(request, 'data_visualisation/dashboard.html', context)

def update_financial_status_with_single_excpense(user, expense_amount, expense_amount_type, expense_category):
    try:
        categories = Category.objects.all()

        for category in categories:
            category_instance = Category.objects.get(name=category.name)
            financial_status = FinancialStatus.objects.get(user=user, category=category_instance)

            if str(category) == str(expense_category.name) and str(expense_amount_type) == "single": #TODO Hard typed type!!
                financial_status.amount -= expense_amount 
                financial_status.save()

                print(financial_status)
                print(financial_status.amount)
    
    except Exception as e:
        print(f"Exception occured in update_financial_status_with_single_earning: {e}")

def delete_expense(request, pk):
    expense = get_object_or_404(ExpensesTracking, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})#TODO Theres no confirm_delete.html

def generate_estimated_expenses_list(request, expense_source_data, financial_status_total_amount):
    # TODO Calculate expenses here
    print("\n---generate_estimated_expenses_list---\n")
    list_of_expenses_per_month = []
    month_sum = 0

    expense_source_data_months = [1,2,3,4,5,6,7,8,9,10,11,12]
    expense_source_data_amount = [entry['amount']  for entry in expense_source_data]
    category = [entry['category']  for entry in expense_source_data]
    
    if expense_source_data_amount:
        for month in expense_source_data_months:
            for expense_source_amount_per_h in expense_source_data_amount:
                month_sum += expense_source_amount_per_h * working_hours_per_month(request, month)  # Expense amount

            list_of_expenses_per_month.append(month_sum + financial_status_total_amount)

        return list_of_expenses_per_month
    else:
        print("LOG: User amount list is empty")
        return redirect('dashboard')
