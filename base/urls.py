from django.urls import path, include
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import RegisterView, InventoryItemViewSet, InventoryChangeViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet, basename='inventory')
router.register(r'changes', InventoryChangeViewSet, basename='changes')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]