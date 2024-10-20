from django.test import TestCase
from firsttuto.LesProduits.models import Fournisseur

class FournisseurModelTest(TestCase):
    """
    Classe de test pour le modèle Fournisseur
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.fournisseur = Fournisseur.objects.create(
            name="Apple")

    def test_fournisseur_creation(self):
        """
        Tester si un fournisseur est bien créé
        """
        self.assertEqual(self.fournisseur.name, "Apple")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Fournisseur
        """
        self.assertEqual(str(self.fournisseur), "{}".format(self.fournisseur.name))

    def test_update_fournisseur(self):
        """
        Tester la mise à jour d'un fournisseur
        """
        self.fournisseur.name = "Samsung"
        self.fournisseur.save()
        # Récupérer l'objet mis à jour
        updated_fournisseur = Fournisseur.objects.get(id=self.fournisseur.id)
        self.assertEqual(updated_fournisseur.name, "Samsung")

    def test_delete_fournisseur(self):
        """
        Tester la suppression d'un fournisseur
        """
        self.fournisseur.delete()
        self.assertEqual(Fournisseur.objects.count(), 0)




