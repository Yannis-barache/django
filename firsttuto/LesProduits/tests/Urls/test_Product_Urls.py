from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from firsttuto.LesProduits.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,ProductDetailView

class ProductTestsUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('product-list')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_create_url_resolves(self):
        url = reverse('product-add')
        self.assertEqual(resolve(url).func.view_class, ProductCreateView)

    def test_update_url_resolves(self):
        url = reverse('product-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductUpdateView)

    def test_delete_url_resolves(self):
        url = reverse('product-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDeleteView)

    def test_detail_url_resolves(self):
        url = reverse('detail_produit', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

class ProductTestUrlResponses(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_create_view_status_code(self):
        """
        Tester que l'URL de création renvoie un statut 200 (OK)
        """
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_status_code(self):
        """
        Tester que l'URL de la liste renvoie un statut 200 (OK)
        """
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

