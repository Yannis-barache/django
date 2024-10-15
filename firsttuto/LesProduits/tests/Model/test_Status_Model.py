from django.test import TestCase
from firsttuto.LesProduits.models import Status

class StatusModelTest(TestCase):
    """
    Classe de test pour le modèle Status
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.status = Status.objects.create(numero=1, libelle="En stock")

    def test_status_creation(self):
        """
        Tester si un status est bien créé
        """
        self.assertEqual(self.status.numero, 1)
        self.assertEqual(self.status.libelle, "En stock")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Status
        """
        self.assertEqual(str(self.status), "{} - {}".format(self.status.numero, self.status.libelle))

    def test_update_status(self):
        """
        Tester la mise à jour d'un status
        """
        self.status.libelle = "En rupture de stock"
        self.status.save()
        # Récupérer l'objet mis à jour
        updated_status = Status.objects.get(id=self.status.id)
        self.assertEqual(updated_status.libelle, "En rupture de stock")

    def test_delete_status(self):
        """
        Tester la suppression d'un status
        """
        self.status.delete()
        self.assertEqual(Status.objects.count(), 0)
