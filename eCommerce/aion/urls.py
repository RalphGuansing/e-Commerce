from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('login/', views.login_view, name='login'),
    path('addproduct/', views.CreateProduct.as_view(), name='addproduct'),
    
    path('product/<int:pk>/', views.ViewProduct.as_view(), name='viewproduct'),
    path('user/<int:pk>/', views.ViewAccount.as_view(), name='viewaccount'),
    path('register/', views.UserFormView.as_view(), name='register'),
    ]
