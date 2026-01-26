from rest_framework import serializers
from .models import Users
from apps.country.serializers import CountrySerializer
from apps.branch.serializers import BranchSerializer


class UserSerializer(serializers.ModelSerializer):
    country_detail = CountrySerializer(source='country', read_only=True)
    branch_detail = BranchSerializer(source='branch', read_only=True)
    
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                  'country', 'country_detail', 'branch', 'branch_detail', 'phone', 
                  'is_active', 'date_joined']
        read_only_fields = ['date_joined']
