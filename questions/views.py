from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Question, Answer
from .forms import SubmitQnForm, SubmitAnsForm
from .filters import QuestionFilter


# Set to lower number for development purposes
ITEMS_PER_PAGE = 3

def index(request):
    # Logged-in users will see all posts listed on home page
    if request.user.is_authenticated:
        # Paginator requires QuerySets to be ordred, and anyway we want most recent questions to appear first
        questions = Question.objects.all().order_by('-datetime_created')

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
    answers = Answer.objects.filter(question__id=qn_id).order_by('-datetime_created')

    ans_paginator = Paginator(answers, ITEMS_PER_PAGE)
    ans_page_number = request.GET.get('page')
    page_answers = ans_paginator.get_page(ans_page_number)

    ansform = SubmitAnsForm()

    return render(request, "questions/question.html", {
        "qn": qn,
        "page_answers": page_answers,
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

def vote_ans(request, ans_id, vote):
    # Query for answer using ans_id
    ans = Answer.objects.get(pk=ans_id)
    
    # Considered: https://stackoverflow.com/questions/2690521/django-check-for-any-exists-for-a-query
    # We need the .all() method: https://stackoverflow.com/questions/17732449/manyrelatedmanager-not-iterable-think-im-trying-to-pull-my-objects-out-incorre
    upvoted = True if request.user in ans.upvoted_by.all() else False
    downvoted = True if request.user in ans.downvoted_by.all() else False
    if vote == "upvote":
        # https://stackoverflow.com/questions/6333068/django-removing-object-from-manytomany-relationship
        if upvoted:
            # Undo user's upvote
            ans.upvoted_by.remove(request.user) 
        elif downvoted:
            # Remove user from downvoted_by
            ans.downvoted_by.remove(request.user)
            ans.upvoted_by.add(request.user)
        else:
            # If user hasn't voted at all, add user
            ans.upvoted_by.add(request.user)
    elif vote == "downvote":
        if upvoted:
            # Remove user from upvoted_by
            ans.upvoted_by.remove(request.user)
            ans.downvoted_by.add(request.user)
        elif downvoted:
            # Undo user's downvote
            ans.downvoted_by.remove(request.user)
        else:
            # If user hasn't voted at all, add user
            ans.downvoted_by.add(request.user)

    # Get new count, return it and update html
    num_votes = ans.upvoted_by.count() - ans.downvoted_by.count()
    return HttpResponse(f"{num_votes}")

def save_qn(request, qn_id):
    qn = Question.objects.get(pk=qn_id)

    # Unsave if question is already saved
    if request.user in qn.saved_by.all():
        qn.saved_by.remove(request.user)
        return HttpResponse("Unsaved")
    else:
        qn.saved_by.add(request.user)
        return HttpResponse("Saved")
    
def view_savedqns(request):
    saved_qns = request.user.savedqns.all()
    if not saved_qns:
        messages.warning(request, "You don't have any questions saved yet!")
        
    return render(request, "questions/saved_qns.html", {
        "saved_qns": saved_qns
    })

def view_profile(request, username):
    user = User.objects.get(username=username)

    return render(request, "users/profile.html", {
        "user": user
    })

def search(request):
    questions = Question.objects.all()
    # print("IsUserInput", bool(request.GET))

    # Set up filter: We will make GET requests and filter from Questions model
    qn_filter = QuestionFilter(request.GET, queryset=questions)

    # If user inputted any queries set questions to filter results, else empty list
    questions = qn_filter.qs if bool(request.GET) else []

    # Order by step is required by Paginator so we order most recent questions first
    questions = questions.order_by('-datetime_created')

    # Set up pagination
    qn_paginator = Paginator(questions, ITEMS_PER_PAGE)
    qn_page_number = request.GET.get('page')
    page_qns = qn_paginator.get_page(qn_page_number)

    return render(request, 'questions/search.html', {
        "qn_filter": qn_filter,
        "questions": questions,
        "page_qns": page_qns,
    })