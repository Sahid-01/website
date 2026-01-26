from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Users
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.select_related('country', 'branch').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
