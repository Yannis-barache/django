from django.test import TestCase
from firsttuto.LesProduits.forms import ProductForm
from firsttuto.LesProduits.models import Product
from django.utils import timezone
from datetime import datetime


class ProductFormTest(TestCase):
    """
    Classe de test pour le formulaire ProductForm
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.product = Product.objects.create(
            name="Couleur",
            code="1234",
            status=0,
            date_creation=timezone.now()
        )

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = ProductForm(data={
            'name': 'iphone',
            'code': '1235',
            'status': 0,
            'date_creation': timezone.now()
        })
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'code' est manquant
        """
        form = ProductForm(data={
            'name': '',
            'code': '',
            'status': 0,
            'date_creation': timezone.now()
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide

    def test_form_optional_data(self):
        """
        Tester que le formulaire est valide si 'code' est manquant
        """
        form = ProductForm(data={
            'name': 'iphone',
            'status': 0,
            'date_creation': timezone.now()
        })
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        form = ProductForm(data={
            'name': 'iphone',
            'code': '1235',
            'status': 0,
            'date_creation': '2021-09-01 00:00:00'
        })
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.name, 'iphone')
        self.assertEqual(product.code, '1235')
        self.assertEqual(product.status, 0)
        
        # On convertit la chaîne de caractères en objet datetime
        expected_date_creation = timezone.make_aware(
            datetime.strptime('2021-09-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

        self.assertEqual(product.date_creation, expected_date_creation)