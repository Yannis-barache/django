from django.test import SimpleTestCase
from django.urls import reverse, resolve

from firsttuto.LesProduits.views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView

class SupplierTestsUrls(SimpleTestCase):

        def test_list_url_resolves(self):
            url = reverse('supplier-list')
            self.assertEqual(resolve(url).func.view_class, SupplierListView)

        def test_create_url_resolves(self):
            url = reverse('supplier-create')
            self.assertEqual(resolve(url).func.view_class, SupplierCreateView)

        def test_update_url_resolves(self):
            url = reverse('supplier-update', args=[1])
            self.assertEqual(resolve(url).func.view_class, SupplierUpdateView)

        def test_delete_url_resolves(self):
            url = reverse('supplier-delete', args=[1])
            self.assertEqual(resolve(url).func.view_class, SupplierDeleteView)


