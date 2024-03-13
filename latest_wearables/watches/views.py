from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignupForm,AuthenticateForm
from django.contrib.auth import authenticate,logout,login as auth_login,update_session_auth_hash
from . models import Customer,Watch,Order,Cart
from django.views import View
from . forms import AuthenticateForm,CustomerForm,AdminProfileForm,UserProfileForm,ChangePasswordForm


# paypal
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
# end paypal


def navbar(request):
    return render(request, 'watches/navbar.html')

def home(request):
        if  request.user.is_authenticated:
            watch=Watch.objects.filter( categories='Home')
            return render(request,'watches/home.html',{'watch':watch})
        else:
           return  redirect('/login/')

def collections(request):
    watch=Watch.objects.all()
    return render(request, 'watches/collections.html',{'watch':watch})


def aboutus(request):
    return render(request, 'watches/about_us.html')

def cart(request):
    return render(request, 'watches/cart.html')

def account(request):
    return render(request, 'watches/login.html')

def login(request):
    return render(request,'watches/login.html')


def log_out(request):
    logout(request)
    return redirect('/login/')
# .........fake......

def signup(request):
    if request.method == "POST":
        mf=SignupForm(request.POST)
   
        if mf.is_valid():
            mf.save()
            return redirect('/login/')
    else:
        mf=SignupForm()
    return render(request, 'watches/signup.html', {'mf':mf})


def log_in(request):
    if not request.user.is_authenticated: 
        if request.method == 'POST':       
            mf = AuthenticateForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    auth_login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request,'watches/login.html',{'mf':mf})
    else:
        return redirect('/')
    
class watchDetailView(View):
    def get(self,request,id):     # id = It will fetch id of particular watch 
        watch_detail = Watch.objects.get(pk=id)

        #------ code for caculate percentage -----
        if watch_detail.discounted_price !=0:    # fetch discount price of particular watch
            percentage = int(((watch_detail.selling_price-watch_detail.discounted_price)/watch_detail.selling_price)*100)
        else:
            percentage = 0
        # ------ code end for caculate percentage ---------
            
        return render(request,'watches/watch_details.html',{'wd':watch_detail,'percentage':percentage})

def add_to_cart(request, id):    # This 'id' is coming from 'watch.id' which hold the id of current watch , which is passing through {% url 'addtocart' watch.id %} from watch_detail.html 
    if request.user.is_authenticated:
        product = Watch.objects.get(pk=id) # product variable is holding data of current object which is passed through 'id' from parameter
        user=request.user                # user variable store the current user i.e steveroger
        Cart(user=user,product=product).save()  # In cart model current user i.e steveroger will save in user variable and current watch object will be save in product variable
        return redirect('watchdetails', id)       # finally it will redirect to watch_details.html with current object 'id' to display watch after adding to the cart
    else:
        return redirect('login')                # If user is not login it will redirect to login page

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of only current user, and show product available in the cart of the current user.
    return render(request, 'watches/cart.html', {'cart_items': cart_items})

def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)    # If the object is found, it returns the object. If not, it raises an HTTP 404 exception (Http404).
    product.quantity += 1                   
    product.save()
    return redirect('viewcart')

def delete_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    return redirect('viewcart')


def delete(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')




#===================================== Address ============================================

def address(request):
    if request.method == 'POST':
            print(request.user)
            mf =CustomerForm(request.POST)
            print('mf',mf)
            if mf.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= mf.cleaned_data['name']
                address= mf.cleaned_data['address']
                city= mf.cleaned_data['city']
                state= mf.cleaned_data['state']
                pincode= mf.cleaned_data['pincode']
                Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        mf =CustomerForm()
        address = Customer.objects.filter(user=request.user)
    return render(request,'watches/address.html',{'mf':mf,'address':address})


def delete_address(request,id):
    if request.method == 'POST':
        de = Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')

#===================================== Checkout ============================================

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'watches/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})


#===================================== Payment ============================================

def payment(request):

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')


    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)

    #================= Paypal Code ======================================
    
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
    
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Watch',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #==========================================================================================================
    return render(request, 'watches/payment.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address,'paypal':paypal_payment})

#===================================== Payment Success ============================================

def payment_success(request,selected_address_id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user,customer=customer_data,watch=c.product,quantity=c.quantity).save()
        c.delete()
    return render(request,'watches/payment_success.html')


#===================================== Payment Failed ============================================


def payment_failed(request):
    return render(request,'watches/payment_failed.html')

#===================================== Order ====================================================

def order(request):
    ord=Order.objects.filter(user=request.user)
    return render(request,'watches/order.html',{'ord':ord})

#========================================== Buy Now ========================================================
def buynow(request,id):
    watch = Watch.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + watch.discounted_price
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'watches/buynow.html', {'final_price':final_price,'address':address,'watch':watch})


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    watch = Watch.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + watch.discounted_price
    
    address = Customer.objects.filter(user=request.user)
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'watch',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================

    return render(request, 'watches/payment.html', {'final_price':final_price,'address':address,'watch':watch,'paypal':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    
    watch = Watch.objects.get(pk=id)
    Order(user=user,customer=customer_data,watch=watch,quantity=1).save()
   
    return render(request,'watches/buynow_payment_success.html')


def profile(request):
    if request.user.is_authenticated:  # This check wheter user is login, if not it will redirect to login page
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'watches/profile.html',{'name':request.user,'mf':mf})
    else:                                                # request.user returns the username
        return redirect('login')
    


def changepassword(request):                                       # Password Change Form               
    if request.user.is_authenticated:                              # Include old password 
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'watches/changepassword.html',{'mf':mf})
    else:
        return redirect('login')
