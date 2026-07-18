from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'description', 'transaction_type', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-bordered w-full'}),
            'amount': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'category': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'transaction_type': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }
