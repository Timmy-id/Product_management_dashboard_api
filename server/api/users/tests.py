from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from .models import CustomUser
from django.urls import reverse

class UserTests(APITestCase):
    def test_create_user(self):
        data = {'username': 'john', 'email': 'john@example.com', 'is_active': True}
        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'john')