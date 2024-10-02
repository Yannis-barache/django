from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import *

from firsttuto.LesProduits.forms import ProductForm
from firsttuto.LesProduits.models import Product, ProductAttribute


# Create your views here.

def index(request):
    return render(request, 'index.html')


def evan(request, name):
    return render(request, 'evan.html', {'name': name})


class ProductListView(ListView):
    model = Product
    template_name = "ListProducts.html"
    context_object_name = "prdcts"


def About(request):
    return render(request, 'about.html')


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


class ConnectView(LoginView):
    template_name = 'connexion.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print("User is valid, active and authenticated ", user)
            return render(request, 'hello.html', {'titreh1': "hello " + username + ", you're connected"})
        else:
            return render(request, 'connexion.html', {'error': 'Invalid login or password'})


class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'connexion.html')
        else:
            return render(request, 'register.html', {'error': 'Invalid login or password'})


class DisconnectView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, **kwargs):
        print("User is disconnected")
        logout(request)
        return render(request, 'index.html')

def ProductCreate(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('detail_produit', product.id)
    else:
        form = ProductForm()
    return render(request, "new_product.html", {'form': form})