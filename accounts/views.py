from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required
def view_account(request, username):
    user = User.objects.get(username=username)
    args = {'user': user}
    return render(request, 'accounts/view_account.html', args)


@login_required
def view_account_info(request, username):
    user = User.objects.get(username=username)
    args = {'user': user}
    return render(request, 'accounts/view_account_info.html', args)
