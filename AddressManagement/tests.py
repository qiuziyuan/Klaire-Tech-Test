from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient

class AddressTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_invalid_post(self):
        response = self.client.post('/api/addresses/', {})
        self.assertEqual(response.status_code, 400)