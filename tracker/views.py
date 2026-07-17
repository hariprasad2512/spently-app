from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Transaction, Category
import json
#|Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # We will create the 'dashboard' URL in Phase 3
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
    
    return render(request, 'tracker/register.html', {'form': form})

# Login View and Logout View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # We will create the 'dashboard' URL in Phase 3
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'tracker/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

# Dashboard VIew
@login_required(login_url='login_view')
def dashboard(request):
    # 1. Fetch user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # 2. Handle Category Filtering
    category_name = request.GET.get('category')
    if category_name:
        transactions = transactions.filter(category__name=category_name)
        
    # 3. Calculate Total Spent (filtering only 'Expense' types)
    expense_transactions = transactions.filter(transaction_type__iexact='Expense')
    total_spent = expense_transactions.aggregate(Sum('amount'))['amount__sum'] or 0.00
    
    # 4. Fetch categories for the filter dropdown
    categories = Category.objects.all()

    # 5. Prepare Chart Data (Group by Category and Sum Amounts)
    category_data = expense_transactions.values('category__name').annotate(total_sum=Sum('amount'))
    chart_labels = [item['category__name'] for item in category_data]
    # Convert Decimals to floats so they can be serialized to JSON
    chart_totals = [float(item['total_sum']) for item in category_data] 
    
    context = {
        'transactions': transactions,
        'total_spent': total_spent,
        'categories': categories,
        'selected_category': category_name,
        # Safely dump Python lists to JSON strings for the frontend
        'chart_labels': chart_labels,
        'chart_totals': chart_totals,
    }
    return render(request, 'tracker/dashboard.html', context)

# CREATE Transaction
@login_required(login_url='login_view')
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # commit=False allows us to modify the object before saving it to the database
            transaction = form.save(commit=False) 
            transaction.user = request.user # Tie the transaction to the logged-in user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
        
    return render(request, 'tracker/add_transaction.html', {'form': form})


# Creating Update (Edit) and Delete Transactions Views

@login_required(login_url='login_view')
def edit_transaction(request, pk):
    # Fetch the specific transaction, strictly ensuring it belongs to the logged-in user
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Pass the existing instance to the form so it updates rather than creates new
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Pre-fill the form with the existing data
        form = TransactionForm(instance=transaction)
        
    return render(request, 'tracker/edit_transaction.html', {'form': form})

@login_required(login_url='login_view')
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')
        
    return render(request, 'tracker/delete_transaction.html', {'transaction': transaction})
