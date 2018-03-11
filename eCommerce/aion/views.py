from django.shortcuts import render
from django.shortcuts import HttpResponse, render, redirect,HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views import generic
from aion.forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import *

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
#    def get_context_data(self, **kwargs):
#        context = super(HomeView, self).get_context_data(**kwargs)
#        context["loggeduser"] = self.request.user.id
#        context["offers"] = Offer.objects.filter(product_id__user_id = self.request.user.id).order_by('-id')
#        context["itemcount"] = self.request.GET.get('paginate_by', self.paginate_by)
#
#        return context

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
                    return HttpResponseRedirect('/home/')
            
            
                
        return render(request, self.template_name,{'form1':form1,'form2':form2,'form3':form3, 'form4':form4, "title": self.title})

def login_view(request):
	print(request.user)
	title = "Login"
	form = UserLoginForm(request.POST or None)
    
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user= authenticate(username=username, password=password)
		login(request,user)
		return HttpResponseRedirect('/home/')
	return render(request, "aion/login.html",{"form":form, "title": title})

#Add Product
class CreateProductView(CreateView):
    form_class = ProductForm
    template_name = 'addproduct.html'
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(CreateProductView, self).form_valid(form)

#Edit Product
class EditProductView(generic.UpdateView):
    form_class = ProductForm
    template_name = 'addproduct.html'
    
    def get_object(self, queryset=None):
        obj = Product.objects.get(id=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(EditProductView, self).get_context_data(**kwargs)
        context["loggeduser"] = self.request.user.id
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
        context["loggeduser"] = self.request.user.id
#        context["object"] = Product.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model 
        return reverse('home')

    
class ViewProduct(generic.DetailView):
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ViewAccount(generic.DetailView):
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_details"] = User_Details.objects.get(user_id=self.object)
        context["user"] = self.object
        
        return context

