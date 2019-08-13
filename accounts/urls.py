from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path(
        '',
        views.view_update_account,
        name='view_update_account'
    ),
    path(
        '<slug:slug>/',
        views.view_account,
        name='view_account'),
    path(
        'ajax/follow/',
        views.follow_or_unfollow_profile,
        name='follow_or_unfollow_profile'
    ),
    path(
        '<slug:slug>/view/<str:req>/',
        views.view_following_or_followers,
        name='view_following_or_followers'
    ),
]
