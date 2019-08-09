"""post_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('post_it/', include('post_it.urls'))
"""


from accounts import views as account_views
from base import views as error_views
from django.conf import settings
from django.conf.urls import handler403, handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('account/', include('accounts.urls')),
    path('register/', account_views.register, name='register'),
    path('activate/<uidb64>/<token>/', account_views.activate_account, name='activate'),
    path('login/',
          auth_views.LoginView.as_view(
              template_name='accounts/login.html',
              redirect_authenticated_user=True),
          name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('change-password/', account_views.change_password, name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = error_views.error_404
handler403 = error_views.error_403