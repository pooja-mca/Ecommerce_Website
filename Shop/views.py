from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.views import View
from .models import Customer,Product,OrderPlaced,Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.





class ProductView(View):
    def get(self, request):
        if 'q' in request.GET:
            q=request.GET['q']
            product = Product.objects.filter(tital__icontains=q)
        else:
            product=Product.objects.all()
        return render(request,'index.html',{'product':product})
#         Male_shoes= Product.objects.c(category='M')
#         Female_shoes= Product.objects.filter(category='F')
#         Child_shoes= Product.objects.filter(category='C')
#         return render(request,'index.html',{'Male_shoes':Male_shoes,'Female_shoes':Female_shoes,'Child_shoes':Child_shoes})
# # user registration



class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'registration/signup.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! Registered Successfully')
            form.save()
        return render(request,'registration/signup.html',{'form':form})


# def CustomerProfile(request):
#     return render(request,'registration/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm
        return  render(request,'registration/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city= form.cleaned_data['city']
            zipcode= form.cleaned_data['zipcode']
            state= form.cleaned_data['state']

            reg=Customer(user=usr, name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()

            # messages.SUCCESS(request,'Congratulation!! Profile Updated Successfully')
        return render(request,'registration/profile.html',{'form':form,'active':'btn-primary'})



def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'address.html',{'add':add,'active':'btn-primary'})


def productDetails(request,id):
    productDetails = Product.objects.get(id=id)
    return render(request,'productDetails.html',{'productDetails': productDetails})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    print(product_id)
    print(user)
    cart_item = Cart.objects.filter(user=user, product=product_id)
    print(cart_item)
    if  not cart_item.exists():
        product = Product.objects.get(id=product_id)

        Cart(user=user, product=product).save()
    return redirect('/cart')
    # return render(request, 'cart.html',{'carts':cart})


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        amount=0.0
        shipping_amount=70.0
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity *p.product.selling_price)
                amount += tempamount
                totalamount = amount+shipping_amount
            return render(request, 'cart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})

        else:
            return render(request,'emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))

        c.quantity+=1
        c.save()

        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            # total_amount = amount + shipping_amount

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }

    return  JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))

        c.quantity-=1
        c.save()

        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            # total_amount = amount + shipping_amount

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }

    return  JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()

        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data={
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return  JsonResponse(data)

@login_required
def checkout(request):
    user =request.user
    add= Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount =amount +shipping_amount
    return render(request, 'checkout.html',{'add':add, 'totalamount':totalamount,'cart_items':cart_items})

@login_required
def paymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer =Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)

    return render(request,'orders.html',{'order_placed':op})