from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField('Location Name', max_length = 50)

    def __str__(self):
        return self.name
