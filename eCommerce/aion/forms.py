from django.contrib.auth.models import User, Group
from django.forms import modelformset_factory
from django.db.models import Q
from .models import *
from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
#from .backends import *
class ProductManagerForm_2(forms.ModelForm):
    
    def clean(self):
        common_usernames = ['admin','administrator','root','system','guest','operator','super','user1','demo','alex','pos','db2admin']
        cleaned_data = super(ProductManagerForm_2, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if username.lower() in common_usernames:
            self.add_error('username', 'Chosen username is unsecure.')
        return cleaned_data
    
    class Meta:
        model = User
        fields = ('username', 'email')

class AccountingManagerForm_2(forms.ModelForm):

    def clean(self):
        common_usernames = ['admin','administrator','root','system','guest','operator','super','user1','demo','alex','pos','db2admin']
        cleaned_data = super(AccountingManagerForm_2, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if username.lower() in common_usernames:
            self.add_error('username', 'Chosen username is unsecure.')
        return cleaned_data
    
    class Meta:
        model = User
        fields = ('username','email')

class ProductManagerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        common_usernames = ['admin','administrator','root','system','guest','operator','super','user1','demo','alex','pos','db2admin']
        cleaned_data = super(ProductManagerForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if username.lower() in common_usernames:
            self.add_error('username', 'Chosen username is unsecure.')
        return cleaned_data
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class AccountingManagerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        common_usernames = ['admin','administrator','root','system','guest','operator','super','user1','demo','alex','pos','db2admin']
        cleaned_data = super(AccountingManagerForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if username.lower() in common_usernames:
            self.add_error('username', 'Chosen username is unsecure.')
        return cleaned_data
    
    class Meta:
        model = User
        fields = ('username','password','email')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('user_id', 'isPurchased')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        common_usernames = ['admin','administrator','root','system','guest','operator','super','user1','demo','alex','pos','db2admin']
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if username.lower() in common_usernames:
            self.add_error('username', 'Chosen username is unsecure.')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name')
    

class UpdateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        common_usernames = ['admin','administrator','root','system','guest','operator','super','user1','demo','alex','pos','db2admin']
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if username.lower() in common_usernames:
            self.add_error('username', 'Chosen username is unsecure.')
        return cleaned_data
    
    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name')

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User_Details
        exclude = ('user_id','account_type','date_created','time_created','isTemporary')
#        exclude = ('user_id','account_type', "billing_address", "shipping_address")

class AddressDetailsForm(forms.ModelForm):

    class Meta:
        model = Address_Details
        exclude = ('user_id', 'address_type')

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('user_id', 'product_id', 'stars')

#AddressFormSet = forms.modelformset_factory(
#    Address_Details,
#    form=AddressDetailsForm,
#    extra=2,
#                                           )

#AddressInlineFormSet = forms.modelformset_factory(
#    Address_Details,
#    form=AddressDetailsForm,
#    extra2,
#                                           )

class UserLoginForm(forms.Form):
    User = get_user_model()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if username and password:
            user = authenticate(username=username, password= password)
            
            if User.objects.filter(username=username).exists():
                log_user = User.objects.get(username=username)
                if not log_user.check_password(password):
                    raise forms.ValidationError("Incorrect Username or Password")
                elif not log_user.is_active:
                    raise forms.ValidationError("Account is not Active")
            else:
                raise forms.ValidationError("Incorrect Username or Password")
                

        return super(UserLoginForm, self).clean(*args, **kwargs)
