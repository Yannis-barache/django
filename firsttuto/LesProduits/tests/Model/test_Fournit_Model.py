from django.test import TestCase
from firsttuto.LesProduits.models import Fournit, Fournisseur, Product
from django.utils import timezone


class FournitModelTest(TestCase):
    """
    Classe de test pour le modèle Fournit
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.fournisseur = Fournisseur.objects.create(
            name="Apple")
        self.product = Product.objects.create(
            name="iphone",
            code="1234",
            status=0,
            date_creation=timezone.now()
        )
        self.fournit = Fournit.objects.create(
            fournisseur=self.fournisseur,
            product=self.product,
            price_ht=1000,
            price_ttc=1200,
        )

    def test_fournit_creation(self):
        """
        Tester si le fournit est bien créé
        """
        self.assertEqual(self.fournit.fournisseur.name, "Apple")
        self.assertEqual(self.fournit.product.name, "iphone")
        self.assertEqual(self.fournit.price_ht, 1000)
        self.assertEqual(self.fournit.price_ttc, 1200)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Fournit
        """
        self.assertEqual(str(self.fournit), "{} fournit {} à {} HT et {} TTC".format(
                                        self.fournit.fournisseur.name, self.fournit.product.name, self.fournit.price_ht, self.fournit.price_ttc))

    def test_update_fournit(self):
        """
        Tester la mise à jour d'un fournit
        """
        self.fournit.price_ht = 1500
        self.fournit.save()
        updated_fournit = Fournit.objects.get(id=self.fournit.id)
        self.assertEqual(updated_fournit.price_ht, 1500)

    def test_delete_fournit(self):
        """
        Tester la suppression d'un fournit
        """
        self.fournit.delete()
        self.assertEqual(Fournit.objects.count(), 0)


