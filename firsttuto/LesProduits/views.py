"""
Les vues de l'application LesProduits
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, TemplateView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Q
from django.core.mail import send_mail

from firsttuto.LesProduits.forms import ContactUsForm, ProductForm, AttributeForm, ProductItemForm, FournisseurForm, FournitFormSet
from firsttuto.LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Fournisseur, \
    Fournit


class ProductListView(ListView):
    """
    Vue pour afficher la liste des produits
    """
    model = Product
    template_name = "ListProducts.html"
    context_object_name = "prdcts"

    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            # Filtre les produits par nom (insensible à la casse)
            return Product.objects.filter(name__icontains=query)
        # Si aucun terme de recherche, retourner tous les produits
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        return context


def About(request):
    return render(request, 'about.html')


def ContactView(request):
    titreh1 = "Contact us !"
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=
                f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()

    return render(request, "Contact.html", {'titreh1': titreh1, 'form': form})


def EmailSent(request):
    return render(request, 'email-sent.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = "detail_produit.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context


class ConnectView(LoginView):
    """
    Vue pour la connexion de l'utilisateur
    """
    template_name = 'connexion.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print("User is valid, active and authenticated ", user)
            return render(
                request, 'hello.html',
                {'titreh1': "hello " + username + ", you're connected"})
        else:
            return render(request, 'connexion.html',
                          {'error': 'Invalid login or password'})


class RegisterView(TemplateView):
    """
    Vue pour l'inscription de l'utilisateur
    """
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
            return render(request, 'register.html',
                          {'error': 'Invalid login or password'})


class DisconnectView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, **kwargs):
        print("User is disconnected")
        logout(request)
        return render(request, 'disconnected.html')


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
    model = Product
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
    """
    Vue pour supprimer un produit
    """
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('Tous les produits')


@method_decorator(login_required, name='dispatch')
class ProductAttributeListView(ListView):
    """
    Vue pour afficher la liste des attributs
    """
    model = ProductAttribute
    template_name = "product_attribute.html"
    context_object_name = "productattributes"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return ProductAttribute.objects.filter(
                name__icontains=query).prefetch_related(
                    'productattributevalue_set')
        return ProductAttribute.objects.all().prefetch_related(
            'productattributevalue_set')

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView,
                        self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context


@method_decorator(login_required, name='dispatch')
class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "detail_attribute.html"
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView,
                        self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values'] = ProductAttributeValue.objects.filter(
            product_attribute=self.object).order_by('position')
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
    """
    Vue pour mettre à jour un attribut
    """
    model = ProductAttribute
    template_name = 'update_attribute.html'
    form_class = AttributeForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        productattribute = form.save()
        return redirect('attribute-detail', productattribute.id)


@method_decorator(login_required, name='dispatch')
class ProductAttributeDeleteView(DeleteView):
    """
    Vue pour supprimer un attribut
    """
    model = ProductAttribute
    template_name = 'delete_attribute.html'
    success_url = reverse_lazy('attribute-list')


@method_decorator(login_required, name='dispatch')
class ProductItemListView(ListView):
    """
    Vue pour afficher la liste des déclinaisons
    """
    model = ProductItem
    template_name = "list_items.html"
    context_object_name = "productitems"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return ProductItem.objects.filter(
                product__name__icontains=query).select_related('product')
        return ProductItem.objects.select_related('product').prefetch_related(
            'attributes')

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
    """
    Vue pour créer une nouvelle déclinaison
    """
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
    """
    Vue pour supprimer une déclinaison
    """
    model = ProductItem
    template_name = 'delete_item.html'
    success_url = reverse_lazy('item-list')


class SupplierListView(ListView):
    """
    Vue pour afficher la liste des fournisseurs
    """
    model = Fournisseur
    template_name = "Supplier/list_supplier.html"
    context_object_name = "fournisseurs"

    def get_queryset(self):
        return Fournisseur.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SupplierListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des fournisseurs"
        return context


def SupplierDetail(request, pk):
    """
    Vue pour afficher les détails d'un fournisseur

    Arguments:
        - `request`: La requête HTTP
        - `pk`: La clé primaire du fournisseur

    """
    fournisseur = Fournisseur.objects.get(pk=pk)
    fournitures = Fournit.objects.filter(fournisseur=fournisseur)

    return render(request, 'Supplier/detail_supplier.html', {
        'supplier': fournisseur,
        'products': fournitures
    })


class SupplierCreateView(CreateView):
    """
    Vue pour créer un nouveau fournisseur
    """
    model = Fournisseur
    template_name = 'Supplier/new_supplier.html'
    form_class = FournisseurForm
    success_url = reverse_lazy('supplier-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = FournitFormSet(self.request.POST,
                                             instance=self.object)
        else:
            data['formset'] = FournitFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SupplierUpdateView(UpdateView):
    """
    Vue pour mettre à jour un fournisseur
    """
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'Supplier/update_supplier.html'
    success_url = reverse_lazy('supplier-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = FournitFormSet(self.request.POST,
                                             instance=self.object)
        else:
            data['formset'] = FournitFormSet(instance=self.object)
        data['supplier'] = self.object  # Ensure supplier is added to context
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            if "save_and_add_another" in self.request.POST:
                return redirect('supplier-update', pk=self.object.pk)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SupplierDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'Supplier/delete_supplier.html'
    success_url = reverse_lazy('supplier-list')


def SearchView(request):
    query = request.GET.get('search')
    products = Product.objects.filter(Q(name__icontains=query))
    attributes = ProductAttribute.objects.filter(name__icontains=query)
    items = ProductItem.objects.filter(
        Q(code__icontains=query) | Q(product__name__icontains=query))

    context = {
        'query': query,
        'products': products,
        'attributes': attributes,
        'items': items,
    }
    return render(request, 'search_results.html', context)
