from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movements import views

router = DefaultRouter()
router.register(r'stock-movements', views.StockMovementViewSet, basename="stock-movement")

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),    
]