from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('', views.view_update_account, name='view_update_account'),
    path('<slug:slug>/', views.view_account, name='view_account'),
    path('follow/<slug:slug>/<str:operation>/', views.follow_profile, name='follow_profile'),
    path('<slug:slug>/view/<str:req>/', views.view_following_or_followers, name='view_following_or_followers'),
]