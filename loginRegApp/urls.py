from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("newsFeed", views.newsFeed),
    path("logout", views.logout),
    path("login", views.login),
    path("createEvent", views.createEvent),
    path("events/<int:eventID>", views.showEvent),
    path("events/<int:eventID>/delete", views.cancelEvent),
    path("updateEvent/<int:eventID>", views.updateEvent),
    path("users/<int:userid>", views.userDetails)
]
