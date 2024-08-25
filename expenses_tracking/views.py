from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpensesTrackingForm  # Assuming you have a similar form for expenses
from .models import ExpensesTracking  # Assuming you have a similar model for expenses


def add_new_expense(request):
    if request.method == 'POST':
        form = ExpensesTrackingForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')  # Redirect to your desired page after saving
    else:
        form = ExpensesTrackingForm()
    
    context = {'form': form}
    return render(request, 'expenses/add_expense.html', context)

def delete_expense(request, pk):
    expense = get_object_or_404(ExpensesTracking, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})

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
