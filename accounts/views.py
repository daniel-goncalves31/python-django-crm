from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Customer
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


@login_required(login_url='login')
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders': total_orders,
               'total_customers': total_customers, 'total_delivered': total_delivered, 'total_pending': total_pending}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
def customer(request, customer_id):

    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def create_order(request, pk):

    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    formset = OrderFormSet(instance=customer)

    context = {'formset': formset}

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def update_order(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


def register_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"The user {username} was created successffully")
            return redirect('login')

    form = CreateUserForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')
