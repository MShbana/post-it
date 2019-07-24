from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<username>/', views.view_account, name='view_account'),
    path('about/<username>/', views.view_account_info, name='view_account_info'),
]