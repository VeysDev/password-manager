from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Goldbar(models.Model):
    website = models.CharField(max_length=100)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.username + " " + self.website 
        # return self.owner.username + self.website  more readable