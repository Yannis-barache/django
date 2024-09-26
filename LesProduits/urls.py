from django.urls import path
from . import views

urlpatterns = [
    path('toutproduit', views.ProductListView.as_view(), name='Tous les produits'),
    path('contact', views.Contact, name='Contact'),
    path('about', views.About, name='About'),

    path('detail_produit/<pk>', views.ProductDetailView.as_view(), name='detail_produit'),
    path('product_attribute', views.ProductAttributeView.as_view(), name='product_attribute'),

    path('login/', views.ConnectView.as_view(), name='connexion'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),





]