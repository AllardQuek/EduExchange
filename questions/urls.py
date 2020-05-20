from django.urls import path

from . import views

# https://docs.djangoproject.com/en/3.0/ref/urls/
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submitqn", views.submit_qn, name="submitqn"),
    path("question/<int:qn_id>", views.view_qn, name="viewqn"),
    path("submitans/<int:qn_id>", views.submit_ans, name="submitans"),
]