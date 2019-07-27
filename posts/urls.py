from .views import Home
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('', login_required(Home.as_view()), name='home'),
]