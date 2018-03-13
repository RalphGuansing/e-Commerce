from django.urls import path

from . import views

urlpatterns = [
#    path('', views.HomePageView.as_view(), name='home'),
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('login/', views.login_view, name='login'),
    path('addproduct/', views.CreateProductView.as_view(), name='addproduct'),
    path('product/<int:pk>/edit/', views.EditProductView.as_view(), name='editproduct'),
    path('product/<int:pk>/delete/', views.DeleteProductView.as_view(), name='deleteproduct'),

    path('product/<int:pk>/', views.ViewProduct.as_view(), name='viewproduct'),
    path('user/<int:pk>/', views.ViewAccount.as_view(), name='viewaccount'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('cart/', views.CartView.as_view(), name='cart'),
    ]
