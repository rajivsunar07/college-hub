from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# For different plans
class Planner(models.Model):
    title = models.CharField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Planner"
        ordering = ["date", "time"]