from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from firsttuto.LesProduits.models import Fournisseur, Fournit, Product

class FournitCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(
            name="iphone",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )
        self.fournisseur = Fournisseur.objects.create(
            name="Apple"
        )
        self.fournit = Fournit.objects.create(
            fournisseur=self.fournisseur,
            product=self.product,
            price_ht=1000,
            price_ttc=1200,
            stock=0,
        )

    def test_create_view_get(self):
        """
        Tester que la vue de création renvoie le bon template et s'affiche correctement
        """
        response = self.client.get(reverse('supplier-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Supplier/new_supplier.html')

class FournitDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(
            name="iphone",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )
        self.fournisseur = Fournisseur.objects.create(
            name="Apple"
        )
        self.fournit = Fournit.objects.create(
            fournisseur=self.fournisseur,
            product=self.product,
            price_ht=1000,
            price_ttc=1200,
            stock=0,
        )

    def test_detail_view_get(self):
        """
        Tester que la vue de détail renvoie le bon template et s'affiche correctement
        """
        response = self.client.get(reverse('supplier-detail', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Supplier/detail_supplier.html')
        self.assertEqual(response.context['supplier'], self.fournisseur)
        self.assertEqual(response.context['supplier'].name, 'Apple')

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.forms import inlineformset_factory
from firsttuto.LesProduits.models import Fournisseur, Fournit, Product
from firsttuto.LesProduits.forms import FournitForm

class FournitUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(
            name="iphone",
            code="1234",
            status=0,
            date_creation="2021-09-01"
        )
        self.fournisseur = Fournisseur.objects.create(
            name="Apple"
        )
        self.fournit = Fournit.objects.create(
            fournisseur=self.fournisseur,
            product=self.product,
            price_ht=1000,
            price_ttc=1200,
            stock=0,
        )
        self.FournitFormSet = inlineformset_factory(Fournisseur, Fournit, form=FournitForm, extra=1)

    def test_update_view_get(self):
        """
        Tester que la vue de modification renvoie le bon template et affiche le formulaire rempli avec les données de l'objet
        """
        response = self.client.get(reverse('supplier-update', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Supplier/update_supplier.html')
        self.assertEqual(response.context['form'].instance, self.fournisseur)

    def test_update_view_post_valid(self):
        """
        Tester que la vue de modification met à jour l'objet lorsque les données sont valides
        """
        data = {
            'name': 'Changement',
            'fournit_set-TOTAL_FORMS': '1',
            'fournit_set-INITIAL_FORMS': '1',
            'fournit_set-MIN_NUM_FORMS': '0',
            'fournit_set-MAX_NUM_FORMS': '1000',
            'fournit_set-0-id': str(self.fournit.id),
            'fournit_set-0-fournisseur': str(self.fournisseur.id),
            'fournit_set-0-product': str(self.product.id),
            'fournit_set-0-price_ht': '1100',
            'fournit_set-0-price_ttc': '1320',
        }
        response = self.client.post(reverse('supplier-update', args=[self.fournisseur.id]), data)
        self.assertEqual(response.status_code, 302)  # Assuming a redirect on success
        self.fournisseur.refresh_from_db()
        print(self.fournit.stock)
        self.fournit.refresh_from_db()
        print(self.fournit.stock)
        self.assertEqual(self.fournisseur.name, 'Changement')
        self.assertEqual(self.fournit.price_ht, 1100)
        self.assertEqual(self.fournit.price_ttc, 1320)


    def test_update_view_post_invalid(self):
        data = {
            'name': 'Apple',
            'fournit_set-TOTAL_FORMS': '1',
            'fournit_set-INITIAL_FORMS': '1',
            'fournit_set-MIN_NUM_FORMS': '0',
            'fournit_set-MAX_NUM_FORMS': '1000',
            'fournit_set-0-id': str(self.fournit.id),
            'fournit_set-0-fournisseur': '100000',
            'fournit_set-0-product': str(self.product.id),
            'fournit_set-0-price_ht': '1100',
            'fournit_set-0-price_ttc': '1320',
        }
        response = self.client.post(reverse('supplier-update', args=[self.fournisseur.id]), data)
        self.assertEqual(response.status_code, 200)












