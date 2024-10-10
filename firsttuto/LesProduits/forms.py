"""
Ce fichier est un fichier de formulaire pour les modèles de l'application LesProduits.
"""
from django import forms
from firsttuto.LesProduits.models import Product, ProductAttribute, ProductItem, Fournisseur, Fournit


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


FournitFormSet = forms.inlineformset_factory(Fournisseur,
                                             Fournit,
                                             form=FournitForm,
                                             extra=1)
