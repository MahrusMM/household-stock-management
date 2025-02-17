from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, Request, Budget
from .forms import RegisterForm, LoginForm, StockForm

# ✅ Dashboard View
@login_required(login_url='login')
def dashboard(request):
    stock_items = Stock.objects.all()
    requests = Request.objects.filter(status="Pending")

    try:
        budget = Budget.objects.get(parent=request.user)
    except Budget.DoesNotExist:
        budget = None

    return render(request, 'stock/dashboard.html', {
        'stock_items': stock_items,
        'requests': requests,
        'budget': budget,
    })


# ✅ View Stock
@login_required(login_url='login')
def view_stock(request):
    """ View stock items & add new stock """
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock item added successfully!")
            return redirect('view_stock')  # Refresh page
    else:
        form = StockForm()

    stock_items = Stock.objects.all()
    return render(request, 'stock/view_stock.html', {'stock_items': stock_items, 'form': form})


# ✅ Delete Stock
@login_required(login_url='login')
def delete_stock(request, item_id):
    """ Delete a stock item """
    item = get_object_or_404(Stock, id=item_id)
    item.delete()
    messages.success(request, "Stock item deleted!")
    return redirect('view_stock')


# ✅ View Requests
@login_required(login_url='login')
def view_requests(request):
    """ View all stock requests """
    requests = Request.objects.all()
    return render(request, 'stock/view_requests.html', {'requests': requests})


# ✅ Settings Page
@login_required(login_url='login')
def settings_page(request):
    return render(request, 'stock/settings.html')


# ✅ Request Stock
@login_required(login_url='login')
def request_stock(request):
    """ Allow child users to request stock items """
    if request.method == "POST":
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])
        item = get_object_or_404(Stock, id=item_id)

        if item.quantity >= quantity:
            Request.objects.create(user=request.user, item=item, quantity=quantity, status="Pending")
            messages.success(request, "Stock request submitted!")
            return redirect('dashboard')
        else:
            messages.error(request, "Not enough stock available!")

    stock_items = Stock.objects.all()
    return render(request, 'stock/request_stock.html', {'stock_items': stock_items})


# ✅ Approve Stock Request
@login_required(login_url='login')
def approve_request(request, request_id):
    """ Approve a stock request and deduct stock """
    stock_request = get_object_or_404(Request, id=request_id)
    
    if stock_request.item.quantity >= stock_request.quantity:
        stock_request.item.quantity -= stock_request.quantity  # Deduct stock
        stock_request.item.save()
        stock_request.status = "Approved"
        stock_request.save()
        messages.success(request, "Stock request approved!")
    else:
        messages.error(request, "Not enough stock available!")

    return redirect('view_requests')


# ✅ Reject Stock Request
@login_required(login_url='login')
def reject_request(request, request_id):
    """ Reject a stock request """
    stock_request = get_object_or_404(Request, id=request_id)
    stock_request.status = "Rejected"
    stock_request.save()
    messages.success(request, "Stock request rejected!")
    return redirect('view_requests')


# ✅ Register User
def register(request):
    """ Handle user registration """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'stock/register.html', {'form': form})


# ✅ User Login
def user_login(request):
    """ Handle user login """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials!")
    else:
        form = LoginForm()

    return render(request, 'stock/login.html', {'form': form})


# ✅ User Logout
def user_logout(request):
    """ Handle user logout """
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')

# ✅ Add Stock Function (Fix for missing 'add_stock' error)
@login_required(login_url='login')
def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock item added successfully!")
            return redirect('view_stock')
        else:
            messages.error(request, "Failed to add stock. Check inputs!")
    
    return redirect('view_stock')  # Redirect to stock page in case of errors

# ✅ View Stock
@login_required(login_url='login')
def view_stock(request):
    stock_items = Stock.objects.all()
    form = StockForm()
    return render(request, 'stock/view_stock.html', {'stock_items': stock_items, 'form': form})

# ✅ Delete Stock
@login_required(login_url='login')
def delete_stock(request, item_id):
    item = get_object_or_404(Stock, id=item_id)
    item.delete()
    messages.success(request, "Stock item deleted!")
    return redirect('view_stock')
