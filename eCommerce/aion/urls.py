from django.urls import path, include
#from axes.decorators import watch_login
from . import views
import django.views.defaults

urlpatterns = [
    
#    path('404/', django.views.defaults.page_not_found, ),
#    path('', views.HomePageView.as_view(), name='home'),
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('product/<int:pk>/', views.ViewProduct.as_view(), name='viewproduct'),
    path('user/<int:pk>/', views.ViewAccount.as_view(), name='viewaccount'),
    path('404/', views.ErrorView.as_view(), name='error404'),
    
    #THE OWNER OF THE ACCOUNT
    path('user/<int:pk>/edit/', views.user_edit, name='editaccount'),
    
    #Accounting Manager and Product Manager
    path('user/<int:pk>/manager/edit/', views.user_manager_edit, name='editmanageraccount'),
    
    #Customer
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/order/<int:pk>/delete', views.delete_order, name='delete-order'),
    path('checkout/',views.CheckoutView.as_view(), name='checkout'),
    path('checkout/submit/', views.PlacedOrder, name = "placedorder"),
    path('product/<int:pk>/add_to_cart', views.add_to_cart, name='add-to-cart'),
    path('product/<int:pk>/add_review', views.CreateReviewView.as_view(), name='add-review'),
    
     path('transactions/', views.TransactionView.as_view(), name='transactions'),
    #Customer and AM
     path('transactions/cart/<int:pk>/', views.Detail_CartView.as_view(), name='detailcart'),
    #Accounting Manager
     path('AM/transactions/', views.AMTransactionView.as_view(), name='transactionsAM'),
     path('AM/transactions/cart/<int:pk>/', views.AMCartView.as_view(), name='amcart'),
     path('AM/transactions/user/<int:pk>/', views.AMUser_TransactionView.as_view(), name='usertransactionsAM'),
    
    #Product Manager
     path('addproduct/', views.CreateProductView.as_view(), name='addproduct'),
     path('product/<int:pk>/edit/', views.EditProductView.as_view(), name='editproduct'),
     path('product/<int:pk>/delete/', views.DeleteProductView.as_view(), name='deleteproduct'),
    
    #Administrator
    path('administrator/', views.AdminView.as_view(), name='administrator'),
    path('createProductManager/', views.ProductManagerFormView.as_view(), name='createProductManager'),
    path('createAccountingManager/', views.AccountingManagerFormView.as_view(), name='createAccountingManager'),
    #path('session_security/', include('session_security.urls')),
    ]
