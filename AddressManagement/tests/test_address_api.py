from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from AddressManagement.models import Address

class AddressApiTests(APITestCase):

    def test_create_address_missing_q(self):
        """
        Tester que l'API retourne 400 Bad Request si le champ 'q' est manquant.
        """
        url = '/api/addresses/'
        data = {}  # Pas de champ 'q'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_address_empty_q(self):
        """
        Tester que l'API retourne 400 Bad Request si le champ 'q' est vide.
        """
        url = '/api/addresses/'
        data = {"q": ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('AddressManagement.views.requests.get')
    def test_create_address_external_api_failure(self, mock_get):
        """
        Tester que l'API retourne 500 si l'API externe échoue.
        """
        mock_get.side_effect = Exception("API request failed")

        url = '/api/addresses/'
        data = {"q": "67 rue de mandres"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    @patch('AddressManagement.views.requests.get')
    def test_create_address_not_found(self, mock_get):
        """
        Tester que l'API retourne 404 si aucune adresse n'est trouvée.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "features": []  # Aucun résultat
        }

        url = '/api/addresses/'
        data = {"q": "adresse inconnue"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    @patch('AddressManagement.views.requests.get')
    def test_create_address_success(self, mock_get):
        """
        Tester que l'API peut enregistrer une adresse avec succès.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "features": [{
                "properties": {
                    "label": "67 Rue de Mandres 91800 Brunoy",
                    "housenumber": "67",
                    "street": "Rue de Mandres",
                    "postcode": "91800",
                    "citycode": "91114"
                },
                "geometry": {
                    "coordinates": [2.518272, 48.705268]
                }
            }]
        }

        url = '/api/addresses/'
        data = {"q": "67 rue de mandres"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(response.data['postcode'], '91800')

    @patch('AddressManagement.views.requests.get')
    def test_get_risks_success(self, mock_get):
        """
        Tester que l'API retourne les risques associés à une adresse existante.
        """
        address = Address.objects.create(
            label="67 Rue de Mandres 91800 Brunoy",
            housenumber="67",
            street="Rue de Mandres",
            postcode="91800",
            citycode="91114",
            latitude=48.705268,
            longitude=2.518272
        )

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"risques": "exemple de risques"}

        url = f'/api/addresses/{address.id}/risks/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('risques', response.data)

    def test_get_risks_address_not_found(self):
        """
        Tester que l'API retourne 404 si l'adresse n'existe pas en base.
        """
        url = '/api/addresses/9999/risks/'  # Un id inexistant
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    @patch('AddressManagement.views.requests.get')
    def test_get_risks_external_api_failure(self, mock_get):
        """
        Tester que l'API retourne 500 si l'appel à l'API Géorisques échoue.
        """
        # Créer une adresse existante
        address = Address.objects.create(
            label="67 Rue de Mandres 91800 Brunoy",
            housenumber="67",
            street="Rue de Mandres",
            postcode="91800",
            citycode="91114",
            latitude=48.705268,
            longitude=2.518272
        )

        # Simuler un échec de l'appel externe
        mock_get.side_effect = Exception("API Georisques failed")

        url = f'/api/addresses/{address.id}/risks/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)