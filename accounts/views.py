from django.shortcuts import render, redirect
from .models import Product, Order, Customer
from django.forms import inlineformset_factory
from .forms import OrderForm


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


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()
    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count}
    return render(request, 'accounts/customer.html', context)


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


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
