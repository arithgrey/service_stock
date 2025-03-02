from django.shortcuts import render
from rest_framework import viewsets
from .models import Warehouse
from .serializers import WarehouseSerializer

# Create your views here.

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer