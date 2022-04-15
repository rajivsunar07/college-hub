from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Groups in the website
class Group(models.Model):
    name = models.CharField(max_length=200, unique=True, default='home')
    group_type = models.CharField(max_length=200)
    user = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name}'

    
    class Meta:
        db_table = "Group"