from django.db import models
from datetime import datetime
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

gender_choice = [(0, "Male"), (1, 'Female')]

# Create your models here.


class Year(models.Model):
    year = models.IntegerField(unique=True)
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.year)


class Movie_Category(models.Model):
    name = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Qualitie(models.Model):
    title = models.CharField(max_length=30)
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=80)
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=300)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=gender_choice, default=0)
    place_of_birth = models.CharField(max_length=300, blank=True)
    biography = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='media/actors/%Y/%m/%d/', blank=True)
    tmdb_id = models.IntegerField(blank=True)
    imdb_id = models.CharField(max_length=10, blank=True)
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    tmdb_id = models.IntegerField()
    name = models.CharField(max_length=250)
    poster = models.ImageField(
        upload_to='media/collections/%Y/%m/%d/', blank=True)
    backdrop = models.ImageField(
        upload_to='media/collections/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=300)
    imdb_title = models.CharField(max_length=300, blank=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    catagory = models.ForeignKey(
        Movie_Category, null=True, on_delete=models.SET_NULL)
    quality = models.ForeignKey(
        Qualitie, blank=True, null=True, on_delete=models.SET_NULL)
    tagline = models.CharField(max_length=600, blank=True)
    overview = models.TextField(blank=True)
    file_path = models.CharField(max_length=500)
    file_size = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    subtitle = models.CharField(max_length=500, blank=True)
    poster = models.ImageField(upload_to='media/movies/%Y/%m/%d/', blank=True)
    backdrop = models.ImageField(upload_to='media/movies/%Y/%m/%d/')
    img_1 = models.ImageField(upload_to='media/movies/%Y/%m/%d/', blank=True)
    img_2 = models.ImageField(upload_to='media/movies/%Y/%m/%d/', blank=True)
    img_3 = models.ImageField(upload_to='media/movies/%Y/%m/%d/', blank=True)
    img_4 = models.ImageField(upload_to='media/movies/%Y/%m/%d/', blank=True)
    tmdb_id = models.IntegerField(blank=True)
    imdb_id = models.CharField(max_length=10, blank=True)
    release_date = models.DateField(blank=True)
    vote_average = models.DecimalField(
        max_digits=2, decimal_places=1, blank=True, default=0)
    vote_count = models.IntegerField(blank=True, default=0)
    views = models.IntegerField(default=0)
    is_pub = models.BooleanField(default=True)
    add_date = models.DateTimeField(default=datetime.now)
    collections = models.ForeignKey(
        Collection,  blank=True, null=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre,  blank=True)
    actors = models.ManyToManyField(Actor,  blank=True)

    def __str__(self):
        return self.title


class Movie_actor_name(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True)
    character = models.CharField(max_length=250)
    cast_num = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.character


class Trailer(models.Model):
    movie = models.ForeignKey(
        Movie,  blank=True, null=True, on_delete=models.SET_NULL)
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    site = models.CharField(max_length=150)
    trailer_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class NeedToDownload(models.Model):
    title = models.CharField(max_length=350, blank=True)
    year = models.IntegerField(blank=True)
    url = models.CharField(max_length=700)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Mojaloss(models.Model):

    title = models.CharField(max_length=350)
    year = models.IntegerField()
    path = models.CharField(max_length=700)

    def __str__(self):
        return self.title
