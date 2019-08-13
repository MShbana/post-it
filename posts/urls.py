from . import views
from .views import Home
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'posts'

urlpatterns = [
    path(
        '',
        login_required(Home.as_view()),
        name='home'
    ),
    path(
        'post/<slug:slug>/',
        views.view_post,
        name='view_post'
    ),
    path(
        'post/<slug:slug>/edit/',
        views.edit_post,
        name='edit_post'
    ),
    path(
        'post/<slug:slug>/delete/',
        views.delete_post,
        name='delete_post'
    ),
]
