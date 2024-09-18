from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from LesProduits.models import Product


# Create your views here.

def index(request):
    return render(request, 'index.html')

def evan(request,name):
    return render(request, 'evan.html', {'name': name})

def ListProducts(request):
    prdcts = Product.objects.all()
    return render(request, 'ListProducts.html', {'prdcts': prdcts})

def About(request):
    return render(request, 'About.html')

def Contact(request):
    return render(request, 'Contact.html')

def detail_produit(request, id):
    prdcts = Product.objects.all()
    if id not in [prdct.id for prdct in prdcts]:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    prdct = Product.objects.get(id=id)


    return render(request, 'detail_produit.html', {'product': prdct})
