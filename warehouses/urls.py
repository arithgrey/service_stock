from rest_framework.routers import DefaultRouter
from django.urls import path, include
from  warehouses import views

router = DefaultRouter()
router.register(r'warehouses', views.WarehouseViewSet,  basename="warehouses")
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
] 