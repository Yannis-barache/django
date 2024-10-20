"""Module contenant les classes d'administration des modèles de l'application LesProduits."""

from django.contrib import admin

from .forms import CommandeProductForm
from .models import (Product, ProductAttribute, ProductAttributeValue,
                     ProductItem, Fournisseur, Fournit, CommandeProduct, Commande)


class FournitInline(admin.TabularInline):
    """
    Classe d'administration pour le modèle Fournit.
    """
    model = Fournit
    extra = 1  # Number of empty forms to display


class ProductItemAdmin(admin.TabularInline):
    """
    Classe d'administration pour le modèle ProductItem.
    """
    model = ProductItem
    filter_vertical = ("attributes",)


class ProductFilter(admin.SimpleListFilter):
    """
    Filtre pour les produits en ligne et hors ligne.
    """
    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin):
        return (
            ('online', 'En ligne'),
            ('offline', 'Hors ligne'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'online':
            return queryset.filter(status=1)
        if self.value() == 'offline':
            return queryset.filter(status=0)


def set_product_online(queryset):
    queryset.update(status=1)
    set_product_online.short_description = "Mettre en ligne"


def set_product_offline(modeladmin, request, queryset):
    queryset.update(status=0)
    set_product_offline.short_description = "Mettre hors ligne"


class ProductAdmin(admin.ModelAdmin):
    model = Production_display = ('name', 'code')
    inlines = [
        ProductItemAdmin,
    ]
    list_display = ["id", "name", "code"]
    list_editable = ["name"]
    radio_fields = {"status": admin.VERTICAL}
    actions = [set_product_online, set_product_offline]
    list_filter = (ProductFilter,)


class FournisseurAdmin(admin.ModelAdmin):
    inlines = [
        FournitInline,
    ]

class CommandeProductInline(admin.TabularInline):
    model = CommandeProduct
    form  = CommandeProductForm
    extra = 0

class CommandeAdmin(admin.ModelAdmin):
    model = Commande
    list_display = ["id", "date_commande", "status"]
    list_editable = ["status"]
    list_filter = ["status"]
    date_hierarchy = "date_commande"
    search_fields = ["id"]
    radio_fields = {"status": admin.HORIZONTAL}
    actions = ["advance_status"]
    inlines = [CommandeProductInline]







admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Fournit)
admin.site.register(Commande, CommandeAdmin)
