from django.contrib import admin
from .models import User, Room, Movie, Review, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Message)
