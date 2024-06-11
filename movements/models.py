from django.db import models

class StockMovement(models.Model):

    MOVEMENT_TYPES = (
        (1, 'entrada'),
        (2, 'salida'),
    )

    product_id = models.IntegerField()
    quantity = models.IntegerField()
    movement_type = models.IntegerField(choices=MOVEMENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display().capitalize()} of {self.quantity} units for product ID {self.product_id} at {self.timestamp}"
