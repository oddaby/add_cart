from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# products/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product
# customers/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerLoginForm

# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import render, redirect
from .models import Order, OrderItem



def products(request):
    # get all products from the database with only the needed fields
    products = Product.objects.values('id', 'name', 'price')
    # create a paginator object with 10 products per page
    paginator = Paginator(products, 10)
    # get the current page number from the request
    page_number = request.GET.get('page')
    # get the current page object from the paginator
    page_obj = paginator.get_page(page_number)
    # render the products list template with the page object context
    return render(request, 'products_list.html', {'page_obj': page_obj})







def customer_login(request):
    # if the request is a POST, try to validate the login form
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            # get the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # try to authenticate the user with the given credentials
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # if the user is authenticated, log them in and redirect to the home page
                login(request, user)
                return redirect('products')
            else:
                # if the user is not authenticated, show an error message
                messages.error(request, 'Invalid username or password.')
    else:
        # if the request is not a POST, create a blank login form
        form = CustomerLoginForm()
    # render the login template with the form context
    return render(request, 'customer_login.html', {'form': form})





@login_required # require the user to be logged in to access this view
def customer_logout(request):
    # log out the current user and redirect to the home page
    logout(request)
    return redirect('home')


def customer_logout(request):
    # log out the current user and redirect to the home page
    logout(request)
    return redirect('home')







from decimal import Decimal
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    # get the product from the database or raise a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    # get or create an order for the current user with a status of 'pending'
    order, created = Order.objects.get_or_create(customer=request.user, status='pending')
    # get or create an order item for the product and the order with a default quantity of 1
    order_item, created = OrderItem.objects.get_or_create(product=product, order=order, defaults={'quantity': 1})
    # if the order item already exists, increment its quantity by 1
    if not created:
        order_item.quantity += 1
        order_item.save()
    # update the total amount of the order by adding the price of the product
    order.total_amount += Decimal(str(product.price))
    order.save()
    # redirect to the cart page
    return redirect('cart')




@login_required    
def cart(request):
    # get the pending order for the current user or None if not exists
    order = Order.objects.filter(customer=request.user, status='pending').first()
    # render the cart template with the order context
    return render(request, 'cart.html', {'order': order})




def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})




# app/views.py



def checkout(request):
    if request.method == 'POST':
        # Retrieve the shipping information from the form
        shipping_name = request.POST.get('name')
        shipping_address = request.POST.get('address')
        
        # Create a new order instance with the shipping information
        order = Order.objects.create(
            customer=request.user,
            total_amount=0,  # Set the total amount appropriately
            status='pending',
            shipping_name=shipping_name,
            shipping_address=shipping_address
        )
        
        # Update the order total amount and save it
        # Logic to calculate and update the total amount
        order.save()
        
        # Redirect to a thank you page or order summary page
        return redirect('order_summary')  # Replace 'order_summary' with the appropriate URL name
    else:
        return render(request, 'checkout.html')
    
    
    
    


@login_required
def order_summary(request):
    # Retrieve the order for the current user with a status of 'pending'
    try:
        order = Order.objects.get(customer=request.user, status='pending')
    except Order.DoesNotExist:
        # Handle the case when no matching order is found
        # You can redirect to a different page or display an error message
        return HttpResponse('No pending order found.')
    except Order.MultipleObjectsReturned:
        # Handle the case when multiple orders are found
        # You can redirect to a different page or display an error message
        return HttpResponse('Multiple pending orders found.')

    # Perform any necessary calculations or data processing
    
    # Render the order summary template with the order object
    return render(request, 'order_summary.html', {'order': order})

