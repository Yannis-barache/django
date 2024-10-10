from django.test import TestCase
from firsttuto.LesProduits.forms import AttributeValueForm
from firsttuto.LesProduits.models import ProductAttribute, ProductAttributeValue


class ProductAttributeValueFormTest(TestCase):
    """
    Classe de test pour le formulaire ProductAttributeValueForm
    """

    def setUp(self):
        """
        Méthode setUp pour initialiser les tests
        """
        self.attribute = ProductAttribute.objects.create(name="Couleur")

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = AttributeForm ( data = { 'value': 'Cyan',
        'product_attribute': self.attribute.id,
        'position': 1} )
        self.assertTrue(form.is_valid()) # Le formulaire doit être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'value' est manquant
        """
        form = ProductAttributeValueForm ( data = { 'product_attribute': self.attribute.id,
        'position': 1 } )
        self.assertFalse(form.is_valid()) # Le formulaire ne doit pas être valide
        self.assertIn('value', form.errors) # Le champ 'value' doit contenir une erreur