from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from base.models import InventoryItem
from rest_framework_simplejwt.tokens import RefreshToken

class InventoryItemCreateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Generate JWT
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_inventory_item(self):
        data = {'name': 'Beef', 'quantity': 10, 'price': '50.00'}
        response = self.client.post('/api/inventory/', data, format='json')
        print(response.status_code, response.data)  # <-- DEBUG
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 1)
