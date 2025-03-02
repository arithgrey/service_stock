from rest_framework import serializers

class StockMovementSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    movement_type = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()

    def validate_movement_type(self, value):
        if value not in [1, 2]:
            raise serializers.ValidationError("Invalid movement type. Please provide 1 for adding or 2 for removing stock.")
        return value

class WarehouseQuantitySerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    warehouse_id = serializers.IntegerField(required=True)
