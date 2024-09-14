# finance/forms.py

from django import forms
from .models import Budget, Category, Transaction
from django import forms


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'month', 'amount']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'transaction_type', 'description']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
