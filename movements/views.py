from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from movements.models import StockMovement
from movements.serializer import StockMovementSerializer, WarehouseQuantitySerializer

class StockMovementService:

    @staticmethod
    def list_product_stock():
        # Obtener los IDs de todos los productos
        product_ids = StockMovement.objects.values_list('product_id', flat=True).distinct()

        # Calcular la cantidad total disponible para cada producto
        products_stock = {}
        for product_id in product_ids:
            success, data = StockMovementService.calculate_stock(product_id)
            if success:
                products_stock[product_id] = data['quantity']

        return products_stock
    
    @staticmethod
    def update_stock(product_id, quantity, movement_type, warehouse_id):
        if movement_type == 1:  # '1' representa una entrada de stock
            StockMovement.objects.create(
                product_id=product_id, 
                quantity=quantity, 
                movement_type=movement_type,
                warehouse_id=warehouse_id
            )
        else:
            StockMovement.objects.create(
                product_id=product_id, 
                quantity=-quantity,
                movement_type=movement_type,
                warehouse_id=warehouse_id
            )
        
        # Calcular el stock total después del movimiento
        return StockMovementService.calculate_stock(product_id)

    @staticmethod
    def calculate_stock(product_id):
        # Sumar todas las cantidades de los movimientos de stock para obtener la cantidad disponible
        total_stock = StockMovement.objects.filter(product_id=product_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        return True, {'product_id': product_id, 'quantity': total_stock if total_stock is not None else 0}

    @staticmethod
    def get_stock(product_id):
        return StockMovementService.calculate_stock(product_id)

    @staticmethod
    def get_stock_by_warehouse(product_id, warehouse_id):
        # Sumar cantidades de movimientos filtrados por producto y almacén
        total_stock = StockMovement.objects.filter(
            product_id=product_id,
            warehouse_id=warehouse_id
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        
        return True, {
            'product_id': product_id,
            'warehouse_id': warehouse_id, 
            'quantity': total_stock if total_stock is not None else 0
        }

class StockMovementViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_movement_service = StockMovementService()

    @action(detail=False, methods=['post'], url_path='existence')
    def stock_existence(self, request):
        data = request.data
        serializer = StockMovementSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = data.get('product_id')
        quantity = data.get('quantity')
        movement_type = data.get('movement_type')  # 1 para agregar, 2 para quitar
        warehouse_id = data.get('warehouse_id')

        
        success, data = self.stock_movement_service.update_stock(
            product_id, quantity, movement_type, warehouse_id)

        if success:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': data}, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=False, methods=['get'], url_path='quantity')
    def stock_quantity(self, request):
        product_id = request.query_params.get('product_id')

        success, data = self.stock_movement_service.get_stock(product_id)

        if success:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': data}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='warehouse-quantity')
    def stock_warehouse_quantity(self, request):
        serializer = WarehouseQuantitySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        success, data = self.stock_movement_service.get_stock_by_warehouse(
            validated_data['product_id'], 
            validated_data['warehouse_id']
        )

        if success:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': data}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='stock-list')
    def stock_list(self, request):
        products_stock = self.stock_movement_service.list_product_stock()

        return Response(products_stock, status=status.HTTP_200_OK)
