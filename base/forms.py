from django import forms
from django.forms import ModelForm
from .models import User, Review, Room, Message
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "username"]


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "bio", "avatar", "username"]

        # making firstname, lastname, email disabled
        widgets = {
            "first_name": forms.TextInput(attrs={"readonly": True}),
            "last_name": forms.TextInput(attrs={"readonly": True}),
            "email": forms.TextInput(attrs={"readonly": True}),
        }

class MovieReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ["review", "rating"]


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = ["name", "description"]


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ["body"]
