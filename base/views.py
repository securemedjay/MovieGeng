from django.shortcuts import redirect, render
from base.models import Movie, Room, Review, User, Message
from base.movie import MovieDisplay
from base.forms import MessageForm, MovieReviewForm, RoomForm, MyUserCreationForm, UserForm, RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


md = MovieDisplay()


def home_view(request):
    search_results = ""
    if request.GET.get("q"):
        q = request.GET.get("q")
        search_results = md.search_TMDB(q)

        for result in search_results:
            print(result)

    context = {
        "search_results": search_results,
        "home": "home",
    }
    return render(request, "home.html", context)


# USER FUNCTIONS

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect("base:home")
        else:
            messages.error(request, 'Password is incorrect')

    page = "login"
    context = {
        "page": page,
    }
    return render(request, "base/login_register.html", context)


def logout_view(request):
    logout(request)
    return redirect("base:home")


def register_view(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("base:home")
        else:
            messages.error(
                request, "An error occurred during registration. Please try again")

    context = {
        "form": form,
    }
    return render(request, "base/login_register.html", context)


def user_profile_view(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()

    context = {
        "user": user,
        "rooms": rooms,
    }
    return render(request, "base/user_profile.html", context)


@login_required(login_url="base:login")
def user_update_view(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("base:user-profile", pk=user.id)

    context = {
        "form": form,
    }
    return render(request, "base/user_profile.html", context)


# MOVIE FUNCTIONS
@login_required(login_url="base:login")
def create_movie_view(request, title_id):
    form = MovieReviewForm()
    movie = md.details(title_id)
    id = movie["id"]
    title = movie["title"]
    image = f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}'
    budget = movie["budget"]
    genres = movie["genres"][0]["name"]
    release_date = movie["release_date"]
    overview = movie["overview"]
    revenue = movie["revenue"]
    # language = movie["spoken_languages"][0]["english_name"]
    duration = movie["runtime"]
    tags = movie["tagline"]
    release_date = movie["release_date"]

    if request.method == "POST":
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            movie, created = Movie.objects.get_or_create(
                name=title,
                tmdb_id=id,
                img_url=image,
                duration=duration,
                overview=overview,
                tags=tags,
                genres=genres,
                budget=budget,
                release_date=release_date,
                # language=language,
                revenue=revenue
            )

            review = Review.objects.create(
                review=request.POST.get("review"),
                rating=request.POST.get("rating"),
                reviewer=request.user
            )
            review.movies.add(movie)

            return redirect("base:movie-list")

    context = {
        "form": form,
        # "movie": movie,
        "title": title,
        "image": image,
        "budget": budget,
        "genres": genres,
        "release_date": release_date,
        "overview": overview,
        "duration": duration,
        # "language": language,
        "tags": tags,
        "revenue": revenue,
    }

    return render(request, "base/create_movie_form.html", context)


def movie_list_view(request):
    w = request.GET.get("w") if request.GET.get("w") else ""
    reviews = Review.objects.filter(
        Q(rating__icontains=w) |
        Q(reviewer__username__icontains=w) |
        Q(review__icontains=w) |
        # filtering reviews by movie name containing the search query
        Q(movies__name__icontains=w)
    )

    # if reviews.count() == 0:
    #     reviews = Review.objects.all()
    # print(reviews)

    total_movie_reviews = reviews.count()
    great_rating_received = reviews.filter(rating="Great").count()
    good_rating_received = reviews.filter(rating="Good").count()
    average_rating_received = reviews.filter(rating="Average").count()
    fair_rating_received = reviews.filter(rating="Fair").count()
    poor_rating_received = reviews.filter(rating="Poor").count()

    if total_movie_reviews == 0:
        total_movie_reviews = Review.objects.all().count()

    great_percent = (great_rating_received/total_movie_reviews) * 100
    good_percent = (good_rating_received/total_movie_reviews) * 100
    average_percent = (average_rating_received/total_movie_reviews) * 100
    fair_percent = (fair_rating_received/total_movie_reviews) * 100
    poor_percent = (poor_rating_received/total_movie_reviews) * 100

    messages = Message.objects.all()

    context = {
        # "movies": movies,
        "reviews": reviews,
        "great_percent": great_percent,
        "good_percent": good_percent,
        "average_percent": average_percent,
        "fair_percent": fair_percent,
        "poor_percent": poor_percent,
        "total_movie_reviews": total_movie_reviews,
        "messages": messages,
    }

    return render(request, "home.html", context)


def movie_detail_view(request, pk, movie_id):
    review = Review.objects.get(id=pk)
    movie = review.movies.get(id=movie_id)

    context = {
        "review": review,
        "movie": movie
    }
    return render(request, "base/movie_detail.html", context)


@login_required(login_url="base:login")
def update_movie_view(request, pk, movie_id):
    review = Review.objects.get(id=pk)
    movie = review.movies.get(id=movie_id)
    form = MovieReviewForm(instance=review)

    if request.method == "POST":
        form = MovieReviewForm(request.POST, instance=review)
        form.save()
        return redirect("base:movie-detail", pk=review.id, movie_id=movie.id)

    context = {
        "review": review,
        "form": form,
        "movie": movie,
    }
    return render(request, "base/update_movie.html", context)


@login_required(login_url="base:login")
def delete_movie_view(request, pk, movie_id):
    review = Review.objects.get(id=pk)
    movie = Movie.objects.get(id=movie_id)
    movie_name = movie.name

    if request.method == "POST":
        review.delete()
        return redirect("base:movie-list")

    context = {
        "object": movie_name,
    }
    return render(request, "base/delete_form.html", context)


# ROOM FUNCTIONS

@login_required(login_url="base:login")
def create_room_view(request, pk):
    # review = Review.objects.get(id=pk)
    movie = None
    if pk != 0:
        movie = Movie.objects.get(id=pk)
    form = RoomForm()
    movies = Movie.objects.all()

    if request.method == "POST":
        form = RoomForm(request.POST)
        movie_name = request.POST.get("movie")
        movie = Movie.objects.get(name=movie_name)

        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.movie = movie
            room.save()
            return redirect("base:room-list")  # to redirect to room-list view

    context = {
        "form": form,
        "movies": movies,
        "movie": movie,
        # "review": review,
    }
    return render(request, "base/room_form.html", context)


def room_list_view(request):
    rooms = Room.objects.all()
    messages = Message.objects.all()

    context = {
        "rooms": rooms,
        "messages": messages,
    }
    return render(request, "base/room_home.html", context)


def room_detail_view(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()
    rooms = Room.objects.all()
    # form = MessageForm()

    if request.method == "POST":
        Message.objects.create(
            writer=request.user,
            room=room,
            body=request.POST.get("message")
        )
        room.participants.add(request.user)
        return redirect("base:room-detail", pk=room.id)

    context = {
        # "form": form,
        "room": room,
        "messages": messages,
        "rooms": rooms,
        "participants": participants,
    }
    return render(request, "base/room_detail.html", context)


@login_required(login_url="base:login")
def update_room_view(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("base:room-detail", pk=room.id)

    context = {
        "form": form,
    }
    return render(request, "base/room_edit_form.html", context)


@login_required(login_url="base:login")
def delete_room_view(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect("base:room-list")

    context = {
        "object": room,
    }
    return render(request, "base/delete_form.html", context)
