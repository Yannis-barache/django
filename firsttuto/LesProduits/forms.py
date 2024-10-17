"""
Ce fichier est un fichier de formulaire pour les modèles de l'application LesProduits.
"""
from django import forms
from django.forms.models import BaseInlineFormSet
from firsttuto.LesProduits.models import Product, ProductAttribute, ProductItem, Fournisseur, Fournit,Commande, CommandeProduct


class BaseCommandeProductFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fournisseur:
            fournisseur = self.instance.fournisseur
            for form in self.forms:
                form.fields['product'].queryset = Product.objects.filter(fournisseurs=fournisseur)

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class AttributeForm(forms.ModelForm):

    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductItemForm(forms.ModelForm):

    class Meta:
        model = ProductItem
        fields = '__all__'


class FournitForm(forms.ModelForm):

    class Meta:
        model = Fournit
        fields = ['product', 'price_ht', 'price_ttc']


class FournisseurForm(forms.ModelForm):

    class Meta:
        model = Fournisseur
        fields = ['name']

    def get_name(self):
        return self.cleaned_data['name']


FournitFormSet = forms.inlineformset_factory(Fournisseur,
                                             Fournit,
                                             form=FournitForm,
                                             extra=1)

class ProductOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Quantité")
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.none(), label="Fournisseur")

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super(ProductOrderForm, self).__init__(*args, **kwargs)
        if product:
            self.fields['fournisseur'].queryset = Fournisseur.objects.filter(fournit__product=product)

class CommandeForm(forms.ModelForm):
    """
    Formulaire pour les commandes
    """
    class Meta:
        model = Commande
        fields = ['fournisseur']
        widgets = {
            'fournisseur': forms.Select(attrs={'id': 'id_fournisseur'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fournisseur'].queryset = Fournisseur.objects.all()
    def assign_user(self, user):
        self.instance.user = user
        self.save()



class CommandeProductForm(forms.ModelForm):
    """
    Formulaire pour les produits commandés
    """
    class Meta:
        model = CommandeProduct
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)

        if instance and instance.commande:
            commande = instance.commande
        elif 'commande' in initial:
            commande = initial['commande']
        else:
            commande = None

        if commande:
            fournisseur = commande.fournisseur
            self.fields['product'].queryset = Product.objects.filter(fournisseurs=fournisseur)

class CommandeStatusForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advance_status'] = forms.BooleanField(
            required=False,
            widget=forms.HiddenInput,
            initial=True
        )


CommandeProductFormSet = forms.inlineformset_factory(
    Commande,
    CommandeProduct,
    form=CommandeProductForm,
    formset=BaseCommandeProductFormSet,
    fields=('product', 'quantity'),
    extra=1
)
