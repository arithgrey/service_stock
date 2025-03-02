from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import Warehouse
from django.utils.text import slugify
from django.apps import apps
from django.db import transaction
from decouple import config

@receiver(post_migrate)
def create_default_warehouse(sender, **kwargs):
    """
    Signal para crear bodegas por defecto después de la migración
    """
    if sender.name == 'warehouses':
        # Usar transaction.atomic() para asegurar que todas las operaciones se completen
        with transaction.atomic():
            # Verificar si ya existen bodegas
            if not Warehouse.objects.exists():
                default_warehouses = [
                    {
                        'name': 'Sur 16',
                        'address': 'Sur 16',
                        'is_active': True
                    },
                    {
                        'name': 'Miguel de la Madrid',
                        'address': 'Miguel de la Madrid',
                        'is_active': True
                    },
                    {
                        'name': 'Venustiano Carranza',
                        'address': 'Venustiano Carranza',
                        'is_active': True
                    },
                    {
                        'name': 'Nezahualcoyotl',
                        'address': 'Nezahualcoyotl',
                        'is_active': True
                    },
                    {
                        'name': 'Auto mazda',
                        'address': 'México',
                        'is_active': True
                    }
                ]
                
                # Crear las bodegas usando bulk_create para mejor rendimiento
                Warehouse.objects.bulk_create([
                    Warehouse(**warehouse) for warehouse in default_warehouses
                ])
                
                print(f"Se crearon {len(default_warehouses)} bodegas por defecto") 