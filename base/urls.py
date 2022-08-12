from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    # Home
    path("", views.movie_list_view, name="home"),

    # Login,Logout,Register
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),

    # Movie
    path("create-movie/<int:title_id>",
         views.create_movie_view, name="create-movie"),
    path("movies/", views.movie_list_view, name="movie-list"),
    path("movie-details/<int:pk>/<int:movie_id>",
         views.movie_detail_view, name="movie-detail"),
    path("movie-update/<int:pk>/<int:movie_id>",
         views.update_movie_view, name="update-movie"),
    path("movie-delete/<int:pk>/<int:movie_id>",
         views.delete_movie_view, name="delete-movie"),

     path("rate/", views.rate_view, name="rate"),
    # Room
    path("create-room/<int:pk>/", views.create_room_view, name="create-room"),
    path("rooms/", views.room_list_view, name="room-list"),
    path("room-detail/<int:pk>/", views.room_detail_view, name="room-detail"),
    path("room-update/<int:pk>/", views.update_room_view, name="update-room"),
    path("room-delete/<int:pk>/",
         views.delete_room_view, name="delete-room"),

    # User
    path("user-profile/<int:pk>/", views.user_profile_view, name="user-profile"),
    path("user-update/", views.user_update_view, name="user-update"),
]
