from django.test import TestCase
from firsttuto.LesProduits.models import Product

class ProductModelTest(TestCase):
    """
    Classe de test pour le modèle Product
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.product = Product.objects.create(
            name="Ipod",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )

    def test_product_creation(self):
        """
        Tester si un produit est bien créé
        """
        self.assertEqual(self.product.name, "Ipod")
        self.assertEqual(self.product.code, "1234")
        self.assertEqual(self.product.status, 0)
        self.assertEqual(self.product.date_creation, "2021-09-01")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Product
        """
        self.assertEqual(str(self.product), "{} - {}".format(self.product.name, self.product.code))

    def test_update_product(self):
        """
        Tester la mise à jour d'un produit
        """
        self.product.name = "iphone"
        self.product.save()
        # Récupérer l'objet mis à jour
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, "iphone")

    def test_delete_product(self):
        """
        Tester la suppression d'un produit
        """
        self.product.delete()
        self.assertEqual(Product.objects.count(), 0)
