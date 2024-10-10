from django.test import TestCase
from firsttuto.LesProduits.models import ProductItem, Product
from django.utils import timezone

class ProductItemModelTest(TestCase):
    """
    Classe de test pour le modèle ProductItem
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.product = Product.objects.create(
            name="iphone",
            code="1234",
            status=0,
            date_creation=timezone.now()
        )
        self.product_item = ProductItem.objects.create(
            product=self.product,
            color="black",
            code="1234",
        )

    def test_product_item_creation(self):
        """
        Tester si un produit est bien créé
        """
        self.assertEqual(self.product_item.product.name, "iphone")
        self.assertEqual(self.product_item.color, "black")
        self.assertEqual(self.product_item.code, "1234")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle ProductItem
        """
        self.assertEqual(str(self.product_item), "{} - {} - {}".format(self.product_item.product.name, self.product_item.color, self.product_item.code))

    def test_update_product_item(self):
        """
        Tester la mise à jour d'un produit
        """
        self.product_item.color = "white"
        self.product_item.save()
        # Récupérer l'objet mis à jour
        updated_product_item = ProductItem.objects.get(id=self.product_item.id)
        self.assertEqual(updated_product_item.color, "white")

    def test_delete_product_item(self):
        """
        Tester la suppression d'un produit
        """
        self.product_item.delete()
        self.assertEqual(ProductItem.objects.count(), 0)
