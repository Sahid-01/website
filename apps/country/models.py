from django.db import models
from apps.common.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)  # NP, AU, IN
    domain = models.CharField(max_length=255, unique=True)  # graceintlgroup.com.au

    def __str__(self):
        return self.name
