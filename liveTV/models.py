from django.db import models
from datetime import datetime

# Create your models here.


class Catagory(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Channel (models.Model):
    name = models.CharField(max_length=350)
    caragory = models.ManyToManyField(Catagory)
    overview = models.TextField(blank=True)
    popular = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='media/liveTv/%Y/%m/%d/')
    backdrop = models.ImageField(
        upload_to='media/liveTv/%Y/%m/%d/', blank=True)
    link_1 = models.CharField(max_length=500)
    link_2 = models.CharField(max_length=500, blank=True)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
