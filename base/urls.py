from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, InventoryItemViewSet, InventoryChangeViewSet, frontend
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet, basename='inventory')
router.register(r'changes', InventoryChangeViewSet, basename='changes')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', frontend, name='frontend'),
    path('add-inventory/', TemplateView.as_view(template_name='add_inventory.html'), name='add_inventory'),
]
