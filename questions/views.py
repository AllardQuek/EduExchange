from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import SubmitQnForm, SubmitAnsForm
from .models import User, Question, Answer


ITEMS_PER_PAGE = 2

def index(request):
    # Logged-in users will see all posts listed on home page
    if request.user.is_authenticated:
        questions = Question.objects.all()

        # https://docs.djangoproject.com/en/3.0/topics/pagination/
        paginator = Paginator(questions, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_qns = paginator.get_page(page_number)
        form = SubmitQnForm()
        
        return render(request, "questions/home.html", {
            "questions": page_qns,
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
            messages.success(request, f"Welcome {request.user}!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "questions/login.html")
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
            messages.error(request, "Passwords do not match!")
            return render(request, "questions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken!")
            return render(request, "questions/register.html")
        login(request, user)
        messages.success(request, f"You have successfully registered. Welcome {request.user}!")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "questions/register.html")

# https://stackoverflow.com/questions/46241383/saving-image-files-in-django-model
def submit_qn(request):
    if request.method == "POST":
        form = SubmitQnForm(request.POST, request.FILES or None)
        if form.is_valid():
            # https://stackoverflow.com/questions/53594745/what-is-the-use-of-cleaned-data-in-django
            # https://stackoverflow.com/questions/46940623/how-to-do-i-automatically-set-the-user-field-to-current-user-in-django-modelform
            qn = form.save(commit=False)
            qn.user = request.user
            qn.save()
            messages.success(request, "Your question was submitted!")

    # Even if someone makes a GET request, they will also be taken to index route
    return HttpResponseRedirect(reverse(index))

@login_required
def view_qn(request, qn_id):
    qn = Question.objects.get(pk=qn_id)

    # Query all answers where question stored has qn_id
    # https://docs.djangoproject.com/en/3.0/topics/db/queries/#filters-can-reference-fields-on-the-model
    # https://stackoverflow.com/questions/1981524/django-filtering-on-foreign-key-properties
    answers = Answer.objects.filter(question__id=qn_id)

    ansform = SubmitAnsForm()

    return render(request, "questions/question.html", {
        "qn": qn,
        "answers": answers,
        "ansform": ansform,
    })

def submit_ans(request, qn_id):
    if request.method == "POST":
        ansform = SubmitAnsForm(request.POST)
        if ansform.is_valid:
            ans = ansform.save(commit=False)
            ans.user = request.user
            ans.question = Question.objects.get(pk=qn_id)
            ans.save()
            messages.success(request, "Your answer has been submitted!")
        # Not sure if need to handle case where form is invalid
        else:
            messages.error(request, "Sorry, we couldn't submit your answer.")

    # https://stackoverflow.com/questions/13202385/django-reverse-with-arguments-and-keyword-arguments-not-found
    return HttpResponseRedirect(reverse(view_qn, args=(qn_id,)))