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
        # 'post/<slug:slug>/edit/',
        'ajax/post/<int:pk>/edit/',
        views.edit_post,
        name='edit_post'
    ),
    path(
        'ajax/post/<int:pk>/edit/cancel/',
        views.cancel_edit_post,
        name='cancel_edit_post'
    ),
    path(
        'post/<int:pk>/delete/',
        views.delete_post,
        name='delete_post'
    ),
    path(
        'comment/<int:pk>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),
    path(
        'ajax/comment/<int:pk>/edit/',
        views.edit_commnet,
        name='edit_comment'
    ),
    path(
        'ajax/comment/<int:pk>/edit/cancel/',
        views.cancel_edit_comment,
        name='cancel_edit_comment'
    ),
    path(
        'ajax/comment/new/',
        views.new_comment,
        name='new_comment'
    ),
    path(
        'ajax/post/new/',
        views.new_post,
        name='new_post'
    ),
]
