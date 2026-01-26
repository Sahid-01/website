from rest_framework import serializers
from .models import Branch
from apps.country.serializers import CountrySerializer


class BranchSerializer(serializers.ModelSerializer):
    country_detail = CountrySerializer(source='country', read_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'code', 'address', 'country', 'country_detail', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
