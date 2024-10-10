from django.test import TestCase
from firsttuto.LesProduits.forms import FournitFormSet
from firsttuto.LesProduits.models import Fournisseur, Fournit, Product
from django.utils import timezone

class FournitFormSetTest(TestCase):
    """
    Classe de test pour le formulaire FournitFormSet
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

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        formset = FournitFormSet(data={
            'fournit_set-TOTAL_FORMS': 1,
            'fournit_set-INITIAL_FORMS': 1,
            'fournit_set-MIN_NUM_FORMS': 0,
            'fournit_set-MAX_NUM_FORMS': 1000,
            'fournit_set-0-id': self.fournit.id,  # Include the id field
            'fournit_set-0-product': self.product.id,
            'fournit_set-0-price_ht': 1000,
            'fournit_set-0-price_ttc': 1200,
        })
        print(formset.errors)
        self.assertTrue(formset.is_valid())  # Le formulaire doit être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'product' est manquant
        """
        formset = FournitFormSet(data={
            'fournit_set-TOTAL_FORMS': 1,
            'fournit_set-INITIAL_FORMS': 1,
            'fournit_set-MIN_NUM_FORMS': 0,
            'fournit_set-MAX_NUM_FORMS': 1000,
            'fournit_set-0-product': '',
            'fournit_set-0-price_ht': 1000,
            'fournit_set-0-price_ttc': 1200,
        })
        self.assertFalse(formset.is_valid())  # Le formulaire ne doit pas être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'price_ht' est manquant
        """
        formset = FournitFormSet(data={
            'fournit_set-TOTAL_FORMS': 1,
            'fournit_set-INITIAL_FORMS': 1,
            'fournit_set-MIN_NUM_FORMS': 0,
            'fournit_set-MAX_NUM_FORMS': 1000,
            'fournit_set-0-product': self.product.id,
            'fournit_set-0-price_ht': '',
            'fournit_set-0-price_ttc': 1200,
        })
        self.assertFalse(formset.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'price_ttc' est manquant
        """
        formset = FournitFormSet(data={
            'fournit_set-TOTAL_FORMS': 1,
            'fournit_set-INITIAL_FORMS': 1,
            'fournit_set-MIN_NUM_FORMS': 0,
            'fournit_set-MAX_NUM_FORMS': 1000,
            'fournit_set-0-product': self.product.id,
            'fournit_set-0-price_ht': 1000,
            'fournit_set-0-price_ttc': '',
        })
        self.assertFalse(formset.is_valid())

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        formset = FournitFormSet(data={
            'fournit_set-TOTAL_FORMS': 1,
            'fournit_set-INITIAL_FORMS': 1,
            'fournit_set-MIN_NUM_FORMS': 0,
            'fournit_set-MAX_NUM_FORMS': 1000,
            'fournit_set-0-id': self.fournit.id,
            'fournit_set-0-product': self.product.id,
            'fournit_set-0-price_ht': 1000,
            'fournit_set-0-price_ttc': 1200,
        })
        print(formset.errors)
        self.assertTrue(formset.is_valid())
        formset.save()
        self.assertEqual(Fournit.objects.count(), 1)
        self.assertEqual(Fournit.objects.get(id=self.fournit.id).price_ht, 1000)
        self.assertEqual(Fournit.objects.get(id=self.fournit.id).price_ttc, 1200)
        self.assertEqual(Fournit.objects.get(id=self.fournit.id).product.name, "iphone")
        self.assertEqual(Fournit.objects.get(id=self.fournit.id).fournisseur.name, "Apple")



    def test_form_save_delete(self):
        formset = FournitFormSet(data={
            'fournit_set-TOTAL_FORMS': 1,
            'fournit_set-INITIAL_FORMS': 1,
            'fournit_set-MIN_NUM_FORMS': 0,
            'fournit_set-MAX_NUM_FORMS': 1000,
            'fournit_set-0-id': self.fournit.id,
            'fournit_set-0-product': self.product.id,
            'fournit_set-0-price_ht': 1000,
            'fournit_set-0-price_ttc': 1200,
            'fournit_set-0-DELETE': True,
        })
        self.assertTrue(formset.is_valid())
        formset.save()
        self.assertEqual(Fournit.objects.count(), 1)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Fournisseur.objects.count(), 1)





