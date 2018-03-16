from django.shortcuts import render
from django.shortcuts import HttpResponse, render, redirect,HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views import generic
from aion.forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

class HomePageView(TemplateView):
    template_name = 'home.html'

class HomeView(generic.ListView):
    template_name = 'aion/home.html'
    context_object_name = 'products'
#    paginate_by = 10
    queryset = Product.objects.all().order_by('-id')

#    def get_paginate_by(self, queryset):
#        self.paginate_by = self.request.GET.get('paginate_by', self.paginate_by)
#        return self.paginate_by
#
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user

        return context
class ProductManagerFormView(generic.View):
    form_class = ProductManagerForm
    second_form_class = UserDetailsForm
    title = "Create Product Manager"
    template_name = 'aion/createProductManager.html'

    #display blank form
    def get(self, request):
        form1 = self.form_class(None)
        form2 = self.second_form_class(None)
        return render(request, self.template_name,{'form1':form1,'form2':form2, "title": self.title})

    #process form data
    def post(self, request):
        form1 = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            user.set_password(password)
            email = form1.cleaned_data['email']
            user.save()
            g = Group.objects.get(name__contains="Product")
            g.user_set.add(user)
#            user.set_password(password)
            g.save()

            user_details = form2.save(commit=False)
            user_details.user_id = user
            user_details.save()


            return HttpResponseRedirect('/administrator/')


class AccountingManagerFormView(generic.View):
    form_class = AccountingManagerForm
    second_form_class = UserDetailsForm
    title = "Create Accounting Manager"
    template_name = 'aion/createAccountingManager.html'

    #display blank form
    def get(self, request):
        form1 = self.form_class(None)
        form2 = self.second_form_class(None)
        return render(request, self.template_name,{'form1':form1,'form2':form2, "title": self.title})

    #process form data
    def post(self, request):
        form1 = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            email = form1.cleaned_data['email']
            user.set_password(password)
            user.save()
            g = Group.objects.get(name__contains="Accounting")
            g.user_set.add(user)
            g.save()

            user_details = form2.save(commit=False)
            user_details.user_id = user
            user_details.save()


            return HttpResponseRedirect('/administrator/')



class UserFormView(generic.View):
    form_class = UserForm
    second_form_class = UserDetailsForm
    bill_form_class = AddressDetailsForm
    ship_form_class = AddressDetailsForm
    title = "Register"
    template_name = 'aion/register.html'

    #display blank form
    def get(self, request):
        form1 = self.form_class(None)
        form2 = self.second_form_class(None)
        form3 = self.bill_form_class(None)
        form4 = self.ship_form_class(None)
        return render(request, self.template_name,{'form1':form1,'form2':form2,'form3':form3, 'form4':form4,"title": self.title})

    #process form data
    def post(self, request):
        form1 = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.bill_form_class(request.POST)
        form4 = self.ship_form_class(request.POST)

        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():

            user = form1.save(commit=False)

            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            user.set_password(password)
            user.save()
            user.groups.add(Group.objects.get(name='Customer'))


            user_details = form2.save(commit=False)
            user_details.user_id = user

            billing_address = form3.save()
            shipping_address = form4.save()

            user_details.billing_address = billing_address
            user_details.shipping_address = shipping_address
            user_details.save()


            #return User objects if credentials are correct
            user = authenticate(username=username,password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/')



        return render(request, self.template_name,{'form1':form1,'form2':form2,'form3':form3, 'form4':form4, "title": self.title})

def user_edit(request, pk):

    if request.method == 'POST':
        user_details = User_Details.objects.get(user_id=request.user)
        form1 = UpdateUserForm(request.POST, instance=request.user)
        form2 = UserDetailsForm(request.POST, instance=user_details)
        form3 = AddressDetailsForm(request.POST, instance=user_details.billing_address)
        form4 = AddressDetailsForm(request.POST, instance=user_details.shipping_address)

        if all([form1.is_valid(), form2.is_valid(), form3.is_valid(), form4.is_valid()]):
            user = form1.save()
            user_details = form2.save(commit=False)
            billing_address = form3.save()
            shipping_address = form4.save()
            
            user_details.billing_address = billing_address
            user_details.shipping_address = shipping_address
            user_details.save()

            return HttpResponseRedirect('/user/'+str(request.user.id)+'/')

    else:
        user_details = User_Details.objects.get(user_id=request.user)
        form1 = UpdateUserForm( instance=request.user)
        form2 = UserDetailsForm( instance=user_details)
        form3 = AddressDetailsForm( instance=user_details.billing_address)
        form4 = AddressDetailsForm( instance=user_details.shipping_address)

    return render(request, 'aion/register.html', {
        'form1':form1,'form2':form2,'form3':form3, 'form4':form4,"title": 'Update'})

def login_view(request):
	print(request.user)
	title = "Login"
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user= authenticate(username=username, password=password)
		login(request,user)
		return HttpResponseRedirect('/')
	return render(request, "aion/login.html",{"form":form, "title": title})

#Add Product
class CreateProductView(CreateView):
    form_class = ProductForm
    template_name = 'addproduct.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(CreateProductView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user
        #context["post_id"] = Offer.objects.get(id=self.kwargs['offer_id']).post_id.id
        return context

class CreateReviewView(CreateView):
    form_class = ReviewForm
    template_name = 'addreview.html'
    
    
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.product_id = Product.objects.get(id=self.kwargs['pk'])
        return super(CreateReviewView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CreateReviewView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user
        #context["post_id"] = Offer.objects.get(id=self.kwargs['offer_id']).post_id.id
        return context

#Edit Product
class EditProductView(generic.UpdateView):
    form_class = ProductForm
    template_name = 'addproduct.html'

    def get_object(self, queryset=None):
        obj = Product.objects.get(id=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditProductView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user
        #context["post_id"] = Offer.objects.get(id=self.kwargs['offer_id']).post_id.id
        return context

#Delete Product
class DeleteProductView(generic.DeleteView):
    model = Product

    def get_object(self, queryset=None):
        obj = Product.objects.get(id=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(DeleteProductView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user
#        context["object"] = Product.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        return reverse('home')


class ViewProduct(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loggeduser"] = self.request.user
        context["request"] = self.request
        context["reviews"] = Review.objects.filter(product_id = self.object)
        
        
        
        return context

class ViewAccount(generic.DetailView):
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_details"] = User_Details.objects.get(user_id=self.object)
        context["user"] = self.object
        context["loggeduser"] = self.request.user
        context["reviews"] = Review.objects.filter(user_id = self.object)

        return context

class SearchView(generic.ListView):
    template_name = 'aion/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(item_name__icontains=self.request.GET.get("search_input", None)).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user
        return context

class CategoryView(generic.ListView):
    template_name = 'aion/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(item_type_slug=self.kwargs['category']).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user

        return context

class CartView(TemplateView):
    template_name = 'aion/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(user_id=self.request.user,isPurchased=False)
        except Cart.DoesNotExist:
            cart = None
        orders = Order.objects.filter(cart_id=cart)

        context["orders"] = orders
        context["cart"] = cart
        context["loggeduser"] = self.request.user

        totalsum = 0;

        for order in orders:
            totalsum += order.item_quantity * order.product_id.item_price

        context["totalsum"] = totalsum
        return context
class AMCartView(TemplateView):
    template_name = 'aion/amcart.html'

    def get_context_data(self, **kwargs):
        context = super(AMCartView, self).get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(id=self.kwargs['pk'],isPurchased=True)
        except Cart.DoesNotExist:
            cart = None
        orders = Order.objects.filter(cart_id=cart)

        context["orders"] = orders
        context["cart"] = cart
        context["loggeduser"] = self.request.user

        totalsum = 0;

        for order in orders:
            totalsum += order.item_quantity * order.product_id.item_price

        context["totalsum"] = totalsum
        return context
    
class Detail_CartView(TemplateView):
    template_name = 'aion/amcart.html'

    def get_context_data(self, **kwargs):
        context = super(Detail_CartView, self).get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(id=self.kwargs['pk'],isPurchased=True)
        except Cart.DoesNotExist:
            cart = None
        orders = Order.objects.filter(cart_id=cart)

        context["orders"] = orders
        context["cart"] = cart
        context["loggeduser"] = self.request.user

        totalsum = 0;

        for order in orders:
            totalsum += order.item_quantity * order.product_id.item_price

        context["totalsum"] = totalsum
        return context

def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return HttpResponseRedirect('/cart/')

#pk of product
def add_to_cart(request, pk):
#    try:
#    go = SomeModel.objects.get(foo='bar')
#except SomeModel.DoesNotExist:
#    go = None
    try:
        CurrentCart = Cart.objects.get(user_id=request.user, isPurchased=False)
    except Cart.DoesNotExist:
        CurrentCart = None

    #if cart does not exists then create
    if CurrentCart is None:
        CurrentCart = Cart(user_id=request.user)
#        CurrentCart.user_id = request.user
        CurrentCart.save()
    try:
        order = Order.objects.get(cart_id=CurrentCart, product_id=pk)
    except Order.DoesNotExist:
        order = None

    if order is None:
        order = Order(cart_id=CurrentCart,product_id=Product.objects.get(pk=pk),item_quantity = 1)
#        order.cart_id = CurrentCart
#        order.product_id = Product.objects.get(pk=pk)
#        order.item_quantity = 1
        order.save()

    else:
        order.item_quantity += 1#quantity
        order.save()


    return HttpResponseRedirect('/cart/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

class CheckoutView(TemplateView):
    template_name = "aion/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user_id=self.request.user,isPurchased=False)
        userDetails = User_Details.objects.get(user_id=self.request.user)

        context["userDetails"] = userDetails
        context["loggeduser"] = self.request.user
        context["cart"] = cart


        return context

def PlacedOrder(request):
    userid = request.user
    cart = Cart.objects.get(user_id=userid, isPurchased=False)
    cart.date_created
    cart.isPurchased = True
    cart.save()

    return HttpResponseRedirect("/")


#by date
#by user
#by amount

class TransactionView(TemplateView):
    template_name= 'aion/transaction_records.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionView, self).get_context_data(**kwargs)

        carts = Cart.objects.filter(user_id=self.request.user,isPurchased=True).order_by('-id')
#        carts = Cart.objects.filter(user_id=self.request.user,isPurchased=True)
        cart_array=[]
        cart_items = {}

        for cart in carts:
            cart_items = {}
            cart_items['cart_id'] = cart.id
            cart_items['date_created'] = cart.date_created
            cart_items['orders'] = Order.objects.filter(cart_id=cart)

            cart_items['totalsum'] = 0
            for order in cart_items['orders']:
                cart_items['totalsum'] += order.item_quantity * order.product_id.item_price
            cart_array.append(cart_items)


        context["carts"] = carts
        context["cart_array"] = cart_array
        context["cart_items"] = cart_items
        context["loggeduser"] = self.request.user

        return context


class AMTransactionView(TemplateView):
    template_name= 'aion/transaction_recordsAM.html'

    def get_context_data(self, **kwargs):
        context = super(AMTransactionView, self).get_context_data(**kwargs)

        carts = Cart.objects.filter(isPurchased=True).order_by('-id')
        cart_array=[]

        for cart in carts:
            cart_items = {}
            cart_items['cart_id'] = cart
            cart_items['date_created'] = cart.date_created
            cart_items['orders'] = Order.objects.filter(cart_id=cart)

            cart_items['totalsum'] = 0
            for order in cart_items['orders']:
                cart_items['totalsum'] += order.item_quantity * order.product_id.item_price
            cart_array.append(cart_items)


        context["carts"] = carts
        context["users"] = User.objects.all()
        context["cart_array"] = cart_array
        context["cart_items"] = cart_items
        context["loggeduser"] = self.request.user

        return context

class AMUser_TransactionView(TemplateView):
    template_name= 'aion/transaction_recordsAM.html'

    def get_context_data(self, **kwargs):
        context = super(AMUser_TransactionView, self).get_context_data(**kwargs)

        carts = Cart.objects.filter(user_id__id=self.kwargs['pk'],isPurchased=True).order_by('-id')
        cart_array=[]
        cart_items = {}

        for cart in carts:
            cart_items = {}
            cart_items['cart_id'] = cart
            cart_items['date_created'] = cart.date_created
            cart_items['time_created'] = cart.time_created
            cart_items['orders'] = Order.objects.filter(cart_id=cart)

            cart_items['totalsum'] = 0
            for order in cart_items['orders']:
                cart_items['totalsum'] += order.item_quantity * order.product_id.item_price
            cart_array.append(cart_items)


        context["carts"] = carts
        context["users"] = User.objects.all()
        context["cart_array"] = cart_array


        context["cart_items"] = cart_items

        context["loggeduser"] = self.request.user

        return context

class AdminView(TemplateView):
    template_name = "aion/admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user

        return context

#class sort_user_AMTransactionView(TemplateView):
#    template_name= 'aion/transaction_recordsAM.html'
#
#    def get_context_data(self, **kwargs):
#        context = super(sort_user_AMTransactionView, self).get_context_data(**kwargs)
#
#        carts = Cart.objects.filter(isPurchased=True).order_by('-user_id')
#        cart_array=[]
#
#        for cart in carts:
#            cart_items = {}
#            cart_items['cart_id'] = cart
#            cart_items['date_created'] = cart.date_created
#            cart_items['orders'] = Order.objects.filter(cart_id=cart)
#
#            cart_items['totalsum'] = 0
#            for order in cart_items['orders']:
#                cart_items['totalsum'] += order.item_quantity * order.product_id.item_price
#            cart_array.append(cart_items)
#
#
#        context["carts"] = carts
#        context["users"] = User.objects.all()
#        context["cart_array"] = cart_array
#        context["cart_items"] = cart_items
#        context["loggeduser"] = self.request.user
#
#        return context
