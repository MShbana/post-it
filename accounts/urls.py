from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('', views.view_update_account, name='view_update_account'),
    path('<slug:slug>/', views.view_account, name='view_account'),
]