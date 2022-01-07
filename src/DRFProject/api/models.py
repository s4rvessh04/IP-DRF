from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.description