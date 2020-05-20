from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PostQnForm
from .models import User, Question


def index(request):
    # Logged-in users will see all posts listed on home page
    if request.user.is_authenticated:
        questions = Question.objects.all()
        form = PostQnForm()
        
        return render(request, "questions/home.html", {
            "questions": questions,
            "form": form,
            })

    # Non-existing users will see a description of website
    else:
        return render(request, "questions/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "questions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "questions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "questions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "questions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "questions/register.html")

# https://stackoverflow.com/questions/46241383/saving-image-files-in-django-model
def submit_qn(request):
    if request.method == "POST":
        form = PostQnForm(request.POST, request.FILES or None)
        if form.is_valid():
            # https://stackoverflow.com/questions/46940623/how-to-do-i-automatically-set-the-user-field-to-current-user-in-django-modelform
            qn = form.save(commit=False)
            qn.user = request.user
            qn.save()

    return HttpResponseRedirect(reverse(index))