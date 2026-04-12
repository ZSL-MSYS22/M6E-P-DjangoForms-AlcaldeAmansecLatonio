# Johann Miguel S. Alcalde, 240150 ; Samantha Louise F. Amansec, 230286 ; Zale Sebastian S. Latonio, 242494
'''
We hereby attest to the truth of the following facts:

We have not discussed the Python code in our program with anyone
other than my instructor or the teaching assistants assigned to this course.

We have not used Python code obtained from another student, or
any other unauthorized source, whether modified or unmodified.

If any Python code or documentation used in our program was
obtained from another source, it has been clearly noted with citations in the
comments of our program.
'''

from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, WaterBottle, Account


def view_suppliers(request):
    suppliers = Supplier.objects.all()
    accounts = Account.objects.all()
    return render(request, 'MyInventoryApp/view_suppliers.html', {'suppliers': suppliers, 'accounts': accounts})

def view_bottles(request):
    water_bottles = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'water_bottles': water_bottles})

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
        return redirect('view_bottles')
    else:
        suppliers = Supplier.objects.all()
        return render(request, 'MyInventoryApp/add_bottle.html', {'suppliers': suppliers})

def view_bottle_details(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)
    return render(request, 'MyInventoryApp/view_bottle_details.html', {'bottle': bottle})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username, password=password)
            # Store pk in session so we can use it across pages
            request.session['account_id'] = account.id
            return redirect('view_suppliers')
        except Account.DoesNotExist:
            return render(request, 'MyInventoryApp/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'MyInventoryApp/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Account.objects.filter(username=username).exists():
            return render(request, 'MyInventoryApp/signup.html', {'error_message': 'Account already exists'})
        else:
            Account.objects.create(username=username, password=password)
            return render(request, 'MyInventoryApp/login.html', {'success_message': 'Account created successfully'})
    else:
        return render(request, 'MyInventoryApp/signup.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def delete_bottle(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)
    bottle.delete()
    return redirect('view_bottles')

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'MyInventoryApp/manage_account.html', {'account': account})

# pk passed via URL; used to filter and delete the specific account record
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    request.session.flush()
    return redirect('login')

# pk passed via URL to identify which account's password to change
def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        currentPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        if currentPassword != account.password:
            return render(request, 'MyInventoryApp/change_password.html', {
                'account': account,
                'error_message': 'Current password is incorrect'
            })
        elif newPassword != confirmPassword:
            return render(request, 'MyInventoryApp/change_password.html', {
                'account': account,
                'error_message': 'New password and confirm password do not match'
            })
        else:
            # Update the specific account record using filter + update
            Account.objects.filter(pk=pk).update(password=newPassword)
            return redirect('manage_account', pk=pk)
    else:
        return render(request, 'MyInventoryApp/change_password.html', {'account': account})
