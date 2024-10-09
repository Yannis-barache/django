from django import forms
from firsttuto.LesProduits.models import Product, ProductAttribute, ProductItem, Fournisseur, Fournit
from django.forms import inlineformset_factory



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

FournitFormSet = inlineformset_factory(Fournisseur, Fournit, form=FournitForm, extra=1)
