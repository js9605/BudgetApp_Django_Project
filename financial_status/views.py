from django.shortcuts import render
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from financial_status.forms import FinancialStatusForm
from financial_status.models import FinancialStatus


User = get_user_model()
def add_new_financial_status(request):
    if request.method == 'POST':
        form = FinancialStatusForm(request.POST)

        if form.is_valid():
            financial_status = form.save(commit=False)
            financial_status.user = request.user
            
            category = form.cleaned_data.get('category')
            entries_exist = FinancialStatus.objects.filter(user=request.user, category=category).exists()

            if entries_exist:
                print("Category exists! Can't add duplicated category!")
            else:
                print("Category does not exist! Adding as new category")
                financial_status.is_created_in_dashboard = True
                financial_status.save()

            return redirect('dashboard')
    else:
        form = FinancialStatusForm()
    
    context = {'form':form}
    return(render(request, 'data_visualisation/dashboard.html', context))

def edit_financial_status(request, financial_status_id):

    financial_status = get_object_or_404(FinancialStatus, id=financial_status_id, user=request.user)
    historical_records_for_category = financial_status.history.filter(category=financial_status.category)

    if request.method == 'POST':
        print("request.method == 'POST' for edit_financial_status")

        form = FinancialStatusForm(request.POST, instance=financial_status) 

        if form.is_valid():
            print("Form is valid for edit_financial_status")
            form.save()
            return redirect('dashboard')
        else:
            print("Form is invalid for edit_financial_status")
            print(form.errors)
    else:
        form = FinancialStatusForm()
    
    context = {
        'form':form,
        'edit_mode':True,
        'financial_status_id':financial_status_id,
        'historical_records_for_category': historical_records_for_category,
    }

    return render(request, 'data_visualisation/edit_financial_status.html', context)
