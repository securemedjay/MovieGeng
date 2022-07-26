from django import forms
from django.forms import ModelForm
from .models import User, Review, Room, Message
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

    # adding form-control class to password1 and password2 fields
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name",
                  "email", "bio", "avatar", "username"]

        # making firstname, lastname, email disabled
        widgets = {
            "email": forms.TextInput(attrs={"readonly": True}),
            "username": forms.TextInput(attrs={"readonly": True}),
            "bio": forms.Textarea(attrs={
                "rows": 5,
                "cols": 30,}),
        }


class MovieReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ["review", "rating"]

        widgets = {
            "review": forms.Textarea(attrs={
                "rows": 5,
                "cols": 30, })
        }


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "size": 30, }),
            "description": forms.Textarea(attrs={
                "rows": 5,
                "cols": 30, })
        }


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ["body"]
