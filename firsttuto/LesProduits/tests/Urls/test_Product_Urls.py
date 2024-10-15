from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from firsttuto.LesProduits.models import Product
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

class ProductTestUrlResponsesWithParameters(TestCase):

        def setUp(self):
            self.product = Product.objects.create(
                name="Ipod",
                code="1234",
                status=0,
                date_creation="2021-09-01"
            )
            self.user = User.objects.create_user(username='testuser', password='secret')
            self.client.login(username='testuser', password='secret')

        def test_update_view_status_code(self):
            """
            Tester que l'URL de modification renvoie un statut 200 (OK)
            """
            url = reverse('product-update', args=[self.product.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


        def test_delete_view_status_code(self):
            """
            Tester que l'URL de suppression renvoie un statut 200 (OK)
            """
            response = self.client.get(reverse('product-delete', args=[self.product.id]))
            self.assertEqual(response.status_code, 200)

        def test_detail_view_status_code(self):
            """
            Tester que l'URL de détail renvoie un statut 200 (OK)
            """
            response = self.client.get(reverse('detail_produit', args=[self.product.id]))
            self.assertEqual(response.status_code, 200)


        def test_detail_view_status_code_invalid_id(self):
            """
            Tester que l'URL de détail renvoie un statut 404 (Not Found) pour un identifiant invalide
            """
            response = self.client.get(reverse('detail_produit', args=[1000]))
            self.assertEqual(response.status_code, 404)

        def test_update_view_status_code_invalid_id(self):
            """
            Tester que l'URL de modification renvoie un statut 404 (Not Found) pour un identifiant invalide
            """
            response = self.client.get(reverse('product-update', args=[1000]))
            self.assertEqual(response.status_code, 404)

        def test_delete_view_status_code_invalid_id(self):
            """
            Tester que l'URL de suppression renvoie un statut 404 (Not Found) pour un identifiant invalide
            """
            response = self.client.get(reverse('product-delete', args=[1000]))
            self.assertEqual(response.status_code, 404)


class ProductTestUrlRedirects(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Ipod",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_create_view_redirect_if_not_logged_in(self):
        """
        Tester que l'URL de création redirige vers la page de connexion si l'utilisateur n'est pas connecté
        """
        self.client.logout()
        response = self.client.get(reverse('product-add'))
        self.assertRedirects(response, '/lesProduits/login/?next=/lesProduits/product/add/')

    def test_update_view_redirect_if_not_logged_in(self):
        """
        Tester que l'URL de modification redirige vers la page de connexion si l'utilisateur n'est pas connecté
        """
        self.client.logout()
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertRedirects(response, '/lesProduits/login/?next=/lesProduits/product/1/update/')

    def test_delete_view_redirect_if_not_logged_in(self):
        """
        Tester que l'URL de suppression redirige vers la page de connexion si l'utilisateur n'est pas connecté
        """
        self.client.logout()
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertRedirects(response, '/lesProduits/login/?next=/lesProduits/product/1/delete/')

    def test_create_view_redirect_if_logged_in(self):
        """
        Tester que l'URL de création redirige vers la page de liste si l'utilisateur est connecté
        """
        response = self.client.post(reverse('product-add'), {
            'name': 'iphone',
            'code': '12345',
            'status': 1,
            'date_creation': '2021-09-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lesProduits/product/2')



    def test_update_view_redirect_if_logged_in(self):
        """
        Tester que l'URL de modification redirige vers la page de liste si l'utilisateur est connecté
        """
        response = self.client.post(reverse('product-update', args=[self.product.id]), {
            'name': 'iphone',
            'code': '12345',
            'status': 1,
            'date_creation': '2021-09-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lesProduits/product/'+str(self.product.id))
