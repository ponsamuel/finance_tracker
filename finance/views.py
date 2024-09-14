# finance/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget, Category, Transaction
from .forms import BudgetForm
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('view_budget')
    else:
        form = BudgetForm()
    
    return render(request, 'finance/set_budget.html', {'form': form})

@login_required
def view_budget(request):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)
    
    budgets = Budget.objects.filter(user=request.user, month__range=[start_of_month, end_of_month])
    transactions = Transaction.objects.filter(user=request.user, date__range=[start_of_month, end_of_month])
    
    budget_dict = {}
    for budget in budgets:
        total_expenses = transactions.filter(category=budget.category, transaction_type='Expense').aggregate(total=Sum('amount'))['total'] or 0
        budget_dict[budget.category.name] = {
            'budget': budget.amount,
            'spent': total_expenses,
            'remaining': budget.amount - total_expenses
        }
    
    context = {
        'budget_dict': budget_dict,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
    }
    
    return render(request, 'finance/view_budget.html', context)

@login_required
def monthly_report(request):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)
    
    transactions = Transaction.objects.filter(user=request.user, date__range=[start_of_month, end_of_month])
    total_income = transactions.filter(transaction_type='Income').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(transaction_type='Expense').aggregate(total=Sum('amount'))['total'] or 0
    savings = total_income - total_expenses
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'transactions': transactions,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
    }
    return render(request, 'finance/monthly_report.html', context)

@login_required
def yearly_report(request):
    now = timezone.now()
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_year = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    
    transactions = Transaction.objects.filter(user=request.user, date__range=[start_of_year, end_of_year])
    total_income = transactions.filter(transaction_type='Income').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(transaction_type='Expense').aggregate(total=Sum('amount'))['total'] or 0
    savings = total_income - total_expenses
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'transactions': transactions,
        'start_of_year': start_of_year,
        'end_of_year': end_of_year,
    }
    return render(request, 'finance/yearly_report.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('view_transactions')
    else:
        form = TransactionForm()
    return render(request, 'finance/add_transaction.html', {'form': form})

@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('view_transactions')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'finance/update_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('view_transactions')
    return render(request, 'finance/delete_transaction.html', {'transaction': transaction})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'finance/view_transactions.html', {'transactions': transactions})
