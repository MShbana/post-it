from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<slug:slug>/', views.view_account, name='view_account'),
    path('info/<slug:slug>/', views.view_account_info, name='view_account_info'),
]