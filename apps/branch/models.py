from django.db import models
from apps.common.models import BaseModel


class Branch(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    country = models.ForeignKey('country.Country', on_delete=models.CASCADE, related_name='branches')
    
    class Meta:
        verbose_name_plural = "Branches"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
