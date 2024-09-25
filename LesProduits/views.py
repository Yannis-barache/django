from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import *
from LesProduits.models import Product, ProductAttribute


# Create your views here.

def index(request):
    return render(request, 'index.html')

def evan(request,name):
    return render(request, 'evan.html', {'name': name})


class ProductListView(ListView):
    model = Product
    template_name = "ListProducts.html"
    context_object_name = "prdcts"


def About(request):
    return render(request, 'About.html')

def Contact(request):
    return render(request, 'Contact.html')

class ProductDetailView(DetailView):
    model = Product
    template_name = "detail_produit.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context

class ProductAttributeView(ListView):
    model = ProductAttribute
    template_name = "product_attribute.html"
    context_object_name = "product_attributes"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context