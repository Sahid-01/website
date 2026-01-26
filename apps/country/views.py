from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Country
from .serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
