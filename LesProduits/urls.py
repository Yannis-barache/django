from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('toutproduit', views.ListProducts, name= "Tous les produits")
]