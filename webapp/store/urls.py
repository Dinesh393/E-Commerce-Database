from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/', views.customers, name='customers'),
    path('orders/', views.orders, name='orders'),
    path('inventory/', views.inventory, name='inventory'),
    path('payments/', views.payments, name='payments'),
    path('reviews/', views.reviews, name='reviews'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-review/', views.add_review, name='add_review'),
    path('database/', views.database, name='database'),
]