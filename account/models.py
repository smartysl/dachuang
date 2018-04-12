from django.db import models
class User(models.Model):
    username=models.CharField(max_length=10)
    password=models.CharField(max_length=10)
    email=models.EmailField()
    def __str__(self):
        return self.username
# Create your models here.
