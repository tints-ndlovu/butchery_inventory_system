from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

#InventoryItemViewSet
from rest_framework import viewsets, permissions, filters
from .models import InventoryItem, InventoryChange
from .serializers import InventoryItemSerializer, InventoryChangeSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here. 
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'New User created successfully', 'user': user.username}, status=status.HTTP_201_CREATED)
    

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    #For filter, search and ordering features
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'quantity', 'date_added']

    def get_queryset(self):
        # Each user sees only their own items
        return InventoryItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        item = self.get_object()
        old_quantity = item.quantity
        updated_item = serializer.save()

        #If the quantity did change it must be logged
        if old_quantity != updated_item.quantity:
            InventoryChange.objects.create(
                item=updated_item,
                user=self.request.user,
                old_quantity=old_quantity,
                new_quantity=updated_item.quantity
            )

class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #Only show changes related to the logged-in user's items
        return InventoryChange.objects.filter(user=self.request.user).order_by('-change_date')