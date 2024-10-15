from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from firsttuto.LesProduits.models import Product

class ProductCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_create_view_get(self):
        """
        Tester que la vue de création renvoie le bon template et s'affiche correctement
        """
        response = self.client.get(reverse('product-add'))  # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Product/new_product.html')

    def test_create_view_post_valid(self):
        """
        Tester que la vue de création crée un nouvel objet lorsque les données sont valides
        """

        data = {
            'name': 'Iphone',
            'code': '1234',
            'status': 0,
            'date_creation': '2021-09-01'
        }
        response = self.client.post(reverse('product-add'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Product.objects.count(), 1)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Product.objects.first().name, 'Iphone')


    def test_create_view_post_invalid(self):
        """
        Tester que la vue de création ne crée pas d'objet lorsque les données sont invalides
        """

        data = {
            'name': '',
            'code': '1234',
            'status': 0,
            'date_creation': '2021-09-01'
        }
        response = self.client.post(reverse('product-add'), data)
        # Vérifie que la page de création est réaffichée avec les erreurs
        self.assertEqual(response.status_code, 200)
        # Vérifie que la vue a bien utilisé le bon template
        self.assertTemplateUsed(response, 'Product/new_product.html')
        # Vérifie que le formulaire contient des erreurs
        self.assertTrue(response.context['form'].errors)

class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Ipod",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les détails de l'objet
        """
        response = self.client.get(reverse('detail_produit', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Product/detail_product.html')
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['product'].name, 'Ipod')


class ProductUpdateViewTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Ipod",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_update_view_get(self):
        """
        Tester que la vue de modification renvoie le bon template et affiche le formulaire rempli avec les données de l'objet
        """
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Product/update_product.html')
        self.assertEqual(response.context['form'].instance, self.product)

    def test_update_view_post_valid(self):
        """
        Tester que la vue de modification met à jour l'objet lorsque les données sont valides
        """
        data = {
            'name': 'Iphone',
            'code': '1234',
            'status': 0,
            'date_creation': '2021-09-01'
        }
        response = self.client.post(reverse('product-update', args=[self.product.id]), data)
        # Vérifie la redirection après la modification
        self.assertEqual(response.status_code, 302)
        # Actualise l'objet depuis la base de données
        self.product.refresh_from_db()
        # Vérifie que l'objet a été modifié
        self.assertEqual(self.product.name, 'Iphone')

    def test_update_view_post_invalid(self):
        """
        Tester que la vue de modification ne modifie pas l'objet lorsque les données sont invalides
        """
        data = {
            'name': '',
            'code': '1234',
            'status': 0,
            'date_creation': '2021-09-01'
        }
        response = self.client.post(reverse('product-update', args=[self.product.id]), data)
        # Vérifie que la page de modification est réaffichée avec les erreurs
        self.assertEqual(response.status_code, 200)
        # Vérifie que la vue a bien utilisé le bon template
        self.assertTemplateUsed(response, 'Product/update_product.html')
        # Actualise l'objet depuis la base de données
        self.product.refresh_from_db()
        # Vérifie que l'objet n'a pas été modifié
        self.assertEqual(self.product.name, 'Ipod')

class ProductDeleteViewTest(TestCase):

        def setUp(self):
            self.product = Product.objects.create(
                name="Ipod",
                code="1234",
                status=0,
                date_creation="2021-09-01"
            )
            self.user = User.objects.create_user(username='testuser', password='secret')
            self.client.login(username='testuser', password='secret')

        def test_delete_view_get(self):
            """
            Tester que la vue de suppression renvoie le bon template
            """
            response = self.client.get(reverse('product-delete', args=[self.product.id]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'Product/delete_product.html')

        def test_delete_view_post(self):
            """
            Tester que la vue de suppression supprime l'objet
            """
            response = self.client.post(reverse('product-delete', args=[self.product.id]))
            # Vérifie la redirection après la suppression
            self.assertEqual(response.status_code, 302)
            # Vérifie que l'objet a été supprimé
            self.assertEqual(Product.objects.count(), 0)





