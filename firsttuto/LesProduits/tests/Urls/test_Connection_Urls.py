from django.test import SimpleTestCase
from django.urls import reverse, resolve

from firsttuto.LesProduits.views import ConnectView, DisconnectView, RegisterView

class ConnectionTestsUrls(SimpleTestCase):

        def test_connect_url_resolves(self):
            url = reverse('connexion')
            self.assertEqual(resolve(url).func.view_class, ConnectView)

        def test_disconnect_url_resolves(self):
            url = reverse('logout')
            self.assertEqual(resolve(url).func.view_class, DisconnectView)

        def test_register_url_resolves(self):
            url = reverse('register')
            self.assertEqual(resolve(url).func.view_class, RegisterView)

