from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import StockMovement

class StockMovementAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_create_movement = reverse('stock-movement-stock-existence')
        self.api_get_quantity = reverse('stock-movement-stock-quantity')
        self.api_stock_list = reverse('stock-movement-stock-list')

    def test_stock_existence(self):
        data = {'product_id': 1, 'quantity': 10, 'movement_type': 1}
        response = self.client.post(self.api_create_movement, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_id'], 1)
        self.assertEqual(response.data['quantity'], 10)

    def test_stock_quantity(self):
        data = {'product_id': 2, 'quantity': 20, 'movement_type': 1}
        self.client.post(self.api_create_movement, data, format='json')
        response = self.client.get(self.api_get_quantity, {'product_id': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data['product_id']), 2)  
        self.assertEqual(response.data['quantity'], 20)

    def test_invalid_movement_type(self):
        data = {'product_id': 3, 'quantity': 5, 'movement_type': 3}
        response = self.client.post(self.api_create_movement, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_product_id(self):
        response = self.client.get(self.api_get_quantity, {'product_id': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data['product_id']), 100)  
        self.assertEqual(response.data['quantity'], 0)

    def test_multiple_stock_movements(self):
        # Agregar varios movimientos de stock para el mismo producto (ID de producto 5)
        product_id = 5
        quantities = [5, 10, -3, 7, -2]  # Cantidades para cada movimiento
        expected_quantity = sum(quantities)  # Calcular la cantidad total esperada después de todos los movimientos
        print(expected_quantity)
        for quantity in quantities:
            data = {'product_id': product_id, 'quantity': abs(quantity), 'movement_type': 1 if quantity > 0 else 2}
            response = self.client.post(self.api_create_movement, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que la cantidad de stock sea la esperada
        response = self.client.get(self.api_get_quantity, {'product_id': product_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data['product_id']), product_id)  
        self.assertEqual(response.data['quantity'], expected_quantity)
