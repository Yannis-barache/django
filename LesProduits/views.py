from django.shortcuts import render
from django.http import HttpResponse

from LesProduits.models import Product


# Create your views here.

def index(request):
    return render(request, 'index.html')

def evan(request,name):
    return render(request, 'evan.html', {'name': name})

def ListProducts(request):
    prdcts = Product.objects.all()
    return render(request, 'ListProducts.html', {'prdcts': prdcts})