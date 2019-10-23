from datetime import datetime
from django.db import models

# Create your models here.


class Catagory (models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TV(models.Model):
    title = models.CharField(max_length=350)
    year = models.IntegerField()
    tmdb_title = models.CharField(max_length=350, blank=True)
    catagory = models.ForeignKey(
        Catagory, on_delete=models.SET_NULL, null=True)
    overview = models.TextField(blank=True)
    poster = models.ImageField(upload_to="media/tv/%Y/%m/%d/", blank=True)
    backdrop = models.ImageField(upload_to="media/tv/%Y/%m/%d/", blank=True)
    tmdb_id = models.IntegerField()
    vote_average = models.DecimalField(
        max_digits=2, decimal_places=1, default=0)
    vote_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class Season (models.Model):
    tv = models.ForeignKey(TV, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tv_season_name = models.CharField(max_length=350)

    def __str__(self):
        return self.tv_season_name


class Episode(models.Model):
    season = models.ForeignKey(Season, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=500)

    def __str__(self):
        return self.name
