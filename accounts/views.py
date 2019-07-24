from django.contrib.auth.models import User
from django.shortcuts import render


def view_account(request, username):
    user = User.objects.get(username=username)
    args = {'user': user}
    return render(request, 'accounts/view_account.html', args)


def view_account_info(request, username):
    user = User.objects.get(username=username)
    args = {'user': user}
    return render(request, 'accounts/view_account_info.html', args)
