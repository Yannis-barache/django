from django.test import SimpleTestCase
from django.urls import reverse, resolve

from firsttuto.LesProduits.views import ProductItemListView, ProductItemCreateView, ProductItemUpdateView, ProductItemDeleteView

class ProductItemTestsUrls(SimpleTestCase):
    """
    Classe de test pour les urls des produits
    """
    def test_list_url_resolves(self):
        url = reverse('item-list')
        self.assertEqual(resolve(url).func.view_class, ProductItemListView)

    def test_create_url_resolves(self):
        url = reverse('item-create')
        self.assertEqual(resolve(url).func.view_class, ProductItemCreateView)

    def test_update_url_resolves(self):
        url = reverse('item-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductItemUpdateView)

    def test_delete_url_resolves(self):
        url = reverse('item-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductItemDeleteView)

