from itertools import product

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from firsttuto.LesProduits.forms import ProductForm, AttributeForm, ProductItemForm
from firsttuto.LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem


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

@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model= Product
    template_name = 'new_product.html'
    form_class = ProductForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('detail_produit', product.id)

@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = ProductForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('detail_produit', product.id)

@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('Tous les produits')



@method_decorator(login_required, name='dispatch')
class ProductAttributeListView(ListView):
    model = ProductAttribute
    template_name = "product_attribute.html"
    context_object_name = "productattributes"

    def get_queryset(self ):
        return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context

@method_decorator(login_required, name='dispatch')
class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "detail_attribute.html"
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values']= ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
        return context

@method_decorator(login_required, name='dispatch')
class ProductAttributeCreateView(CreateView):
    model = ProductAttribute
    template_name = 'new_attribute.html'
    form_class = AttributeForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        productattribute = form.save()
        return redirect('attribute-detail', productattribute.id)

@method_decorator(login_required, name='dispatch')
class ProductAttributeUpdateView(UpdateView):
    model = ProductAttribute
    template_name = 'update_attribute.html'
    form_class = AttributeForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        productattribute = form.save()
        return redirect('attribute-detail', productattribute.id)

@method_decorator(login_required, name='dispatch')
class ProductAttributeDeleteView(DeleteView):
    model = ProductAttribute
    template_name = 'delete_attribute.html'
    success_url = reverse_lazy('attribute-list')

@method_decorator(login_required, name='dispatch')
class ProductItemListView(ListView):
    model = ProductItem
    template_name = "list_items.html"
    context_object_name = "productitems"

    def get_queryset(self):
        return ProductItem.objects.select_related('product').prefetch_related('attributes')

    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des déclinaisons"
        return context

@method_decorator(login_required, name='dispatch')
class ProductItemDetailView(DetailView):
    model = ProductItem
    template_name = "detail_item.html"
    context_object_name = "productitem"

    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"
        # Récupérer les attributs associés à cette déclinaison
        context['attributes'] = self.object.attributes.all()
        return context

@method_decorator(login_required, name='dispatch')
class ProductItemCreateView(CreateView):
    model = ProductItem
    template_name = 'new_item.html'
    form_class = ProductItemForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        productitem = form.save()
        return redirect('item-detail', productitem.id)

@method_decorator(login_required, name='dispatch')
class ProductItemUpdateView(UpdateView):
    model = ProductItem
    template_name = 'update_item.html'
    form_class = ProductItemForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        productitem = form.save()
        return redirect('item-detail', productitem.id)

@method_decorator(login_required, name='dispatch')
class ProductItemDeleteView(DeleteView):
    model = ProductItem
    template_name = 'delete_item.html'
    success_url = reverse_lazy('item-list')


