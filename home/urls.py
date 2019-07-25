from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path


app_name = 'home'

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='home'),
]
