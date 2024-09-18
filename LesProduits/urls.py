from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('toutproduit', views.ListProducts, name= "Tous les produits"),

    path('contact', views.Contact, name='Contact'),
    path('about', views.About, name='About'),

    path('detail_produit/<int:id>', views.detail_produit, name='detail_produit'),



]