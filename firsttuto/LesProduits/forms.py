from django import forms
from firsttuto.LesProduits.models import Product, ProductAttribute, ProductItem


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

