from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, WaterBottle, Account


def view_suppliers(request):
    suppliers = Supplier.objects.all()
    accounts = Account.objects.all()
    return render(request, 'view_suppliers.html', {'suppliers': suppliers, 'accounts': accounts})

def view_water_bottles(request):
    water_bottles = WaterBottle.objects.all()
    return render(request, 'view_water_bottles.html', {'water_bottles': water_bottles})

def add_bottle(request):
    if request.method == 'POST':
        SKU = request.POST.get('SKU')
        brand = request.POST.get('brand')
        cost = request.POST.get('cost')
        size = request.POST.get('size')
        mouth_size = request.POST.get('mouth_size')
        color = request.POST.get('color')
        supplied_by_id = request.POST.get('supplied_by')
        current_quantity = request.POST.get('current_quantity')

        supplied_by = get_object_or_404(Supplier, pk=supplied_by_id)

        WaterBottle.objects.create(
            SKU=SKU,
            brand=brand,
            cost=cost,
            size=size,
            mouth_size=mouth_size,
            color=color,
            supplied_by=supplied_by,
            current_quantity=current_quantity
        )
        return redirect('view_water_bottles')
    else:
        suppliers = Supplier.objects.all()
        return render(request, 'add_bottle.html', {'suppliers': suppliers})

def view_bottle_details(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)
    return render(request, 'view_bottle_details.html', {'bottle': bottle})


def login_view(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username, password=password)
            request.session['account_id'] = account.id
            return redirect('view_water_bottles')
        except Account.DoesNotExist:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Account.objects.filter(username=username).exists():
            error_message = 'Username already exists'
            return render(request, 'signup.html', {'error_message': error_message})
        else:
            account = Account.objects.create(username=username, password=password)
            request.session['account_id'] = account.id
            return redirect('view_water_bottles')
    else:
        return render(request, 'signup.html')
    
def logout_view(request):
    request.session.flush()
    return redirect('login')

def delete_bottle(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)
    bottle.delete()
    return redirect('view_water_bottles')

def manage_account(request):
    account = get_object_or_404(Account, pk=request.session.get('account_id'))
    return render(request, 'manage_account.html', {'account': account})

def delete_account(request):
    account = get_object_or_404(Account, pk=request.session.get('account_id'))
    account.delete()
    request.session.flush()
    return redirect('login') 

def change_password(request):
    account = get_object_or_404(Account, pk=request.session.get('account_id'))
    if request.method == 'POST':
        currentPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword') 
        if currentPassword != account.password:
            error_message = 'Current password is incorrect'
            return render(request, 'change_password.html', {'account': account, 'error_message': error_message})
        elif newPassword != confirmPassword:
            error_message = 'New password and confirm password do not match'
            return render(request, 'change_password.html', {'account': account, 'error_message': error_message})
        else:
            account.password = newPassword
            account.save()
            return redirect('manage_account')







