from django.shortcuts import redirect, render
from base.models import Movie, Room, Review, User, Message
from base.movie import MovieDisplay
from base.forms import MessageForm, MovieReviewForm, RoomForm, MyUserCreationForm, UserForm, RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django_gravatar.helpers import get_gravatar_profile_url, has_gravatar

md = MovieDisplay()
total_movie_reviews = 0
great_percent = 0
good_percent = 0
average_percent = 0
fair_percent = 0
poor_percent = 0

current_year = datetime.now().year


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
        "current_year": current_year,
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
            messages.error(request, 'Username or password is incorrect. Try again')
        else:
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'You have logged in successfully')
                return redirect(request.GET.get("next", "base:home"))  # redirects to next if available else redirects home
            else:
                messages.error(request, 'Username or password is incorrect. Try again')

    page = "login"
    context = {
        "page": page,
    }
    return render(request, "base/login_register.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully")
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
            return redirect(request.GET.get("next", "base:home")) 
        else:
            print(form.errors.as_data())
            messages.error(
                request, "An error occurred during registration. Please try again")

    context = {
        "form": form,
    }
    return render(request, "base/login_register.html", context)


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
    global great_percent, good_percent, average_percent, fair_percent, poor_percent, total_movie_reviews

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

    room_messages = Message.objects.all()

    context = {
        # "movies": movies,
        "reviews": reviews,
        "great_percent": great_percent,
        "good_percent": good_percent,
        "average_percent": average_percent,
        "fair_percent": fair_percent,
        "poor_percent": poor_percent,
        "total_movie_reviews": total_movie_reviews,
        "room_messages": room_messages,
    }

    return render(request, "home.html", context)


def movie_detail_view(request, pk, movie_id):
    review = Review.objects.get(id=pk)
    movie = review.movies.get(id=movie_id)  # getting movies under review

    m = Movie.objects.get(id=movie_id)
    total_movie_reviews = m.review_set.all().count()  # getting reviews under a movie

    great_rating_received = m.review_set.filter(rating="Great").count()
    good_rating_received = m.review_set.filter(rating="Good").count()
    average_rating_received = m.review_set.filter(rating="Average").count()
    fair_rating_received = m.review_set.filter(rating="Fair").count()
    poor_rating_received = m.review_set.filter(rating="Poor").count()

    great_percent = (great_rating_received/total_movie_reviews) * 100
    good_percent = (good_rating_received/total_movie_reviews) * 100
    average_percent = (average_rating_received/total_movie_reviews) * 100
    fair_percent = (fair_rating_received/total_movie_reviews) * 100
    poor_percent = (poor_rating_received/total_movie_reviews) * 100

    context = {
        "review": review,
        "movie": movie,
        "great_percent": great_percent,
        "good_percent": good_percent,
        "average_percent": average_percent,
        "fair_percent": fair_percent,
        "poor_percent": poor_percent,
        "total_movie_reviews": total_movie_reviews,
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

    w = request.GET.get("w") if request.GET.get("w") else ""
    rooms = Room.objects.filter(
        Q(movie__name__icontains=w) |
        Q(host__username__icontains=w)
    )

    # rooms = Room.objects.all()
    room_messages = Message.objects.all()

    context = {
        "rooms": rooms,
        "room_messages": room_messages,
    }
    return render(request, "base/room_home.html", context)


def room_detail_view(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    rooms = Room.objects.all()
    profile_url = get_gravatar_profile_url('alice@example.com')
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
        "room_messages": room_messages,
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


def user_profile_view(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    # use user.review_set.all() instead of user.reviews because user has a one-many relationship with review, otherwise use user.reviews
    reviews = user.review_set.all()
    review_count = user.review_set.all().count()
    room_count = user.room_set.all().count()

    rank = ""
    if review_count < 10:
        rank = "Recruit"
    elif 10 <= review_count < 30:
        rank = "Sergeant"
    elif 30 <= review_count < 60:
        rank = "Lieutenant"
    elif 60 <= review_count < 90:
        rank = "Captain"
    elif 90 <= review_count < 130:
        rank = "Major"
    elif 130 <= review_count < 180:
        rank = "Colonel"
    else:
        rank = "General"

    context = {
        "user": user,
        "rooms": rooms,
        "review_count": review_count,
        "room_count": room_count,
        "rank": rank,
        "great_percent": great_percent,
        "good_percent": good_percent,
        "average_percent": average_percent,
        "fair_percent": fair_percent,
        "poor_percent": poor_percent,
        "total_movie_reviews": total_movie_reviews,
        # "reviews": review,
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
        else:
            print(form.errors.as_data())

    context = {
        "form": form,
        "great_percent": great_percent,
        "good_percent": good_percent,
        "average_percent": average_percent,
        "fair_percent": fair_percent,
        "poor_percent": poor_percent,
        "total_movie_reviews": total_movie_reviews,
    }
    return render(request, "base/user_profile.html", context)
