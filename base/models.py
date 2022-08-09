from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=255)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]


class Movie(models.Model):
    name = models.CharField(max_length=255)
    tmdb_id = models.CharField(max_length=255)
    img_url = models.CharField(null=True, max_length=255)
    # review = models.ForeignKey(Review, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    # plot = models.TextField(null=True)
    overview = models.TextField(null=True)
    tags = models.CharField(max_length=255, null=True)
    genres = models.CharField(max_length=255, null=True)
    budget = models.IntegerField(null=True)
    release_date = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=255, null=True)
    revenue = models.IntegerField(null=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = [
        ("Great", 'Great'),
        ("Good", 'Good'),
        ("Average", 'Average'),
        ("Fair", 'Fair'),
        ("Poor", 'Poor'),
    ]

    # rating = models.IntegerField()
    movies = models.ManyToManyField(Movie)
    review = models.TextField(null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.CharField(
        max_length=7, choices=RATING_CHOICES, default="Average", blank=True)
    # great_percent = models.IntegerField(null=True)
    # good_percent = models.IntegerField(null=True)
    # average_percent = models.IntegerField(null=True)
    # fair_percent = models.IntegerField(null=True)
    # poor_percent = models.IntegerField(null=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-reviewed_at"]

    # name = models.CharField(max_length=10)

    def __str__(self):
        return self.review[0:50]


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        User, related_name="participants")
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Message(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.body[0:50]
