from django.shortcuts import render


def view_account(request, username):
    args = {'user': request.user}
    return render(request, 'accounts/view_account.html', args)


def view_account_info(request, username):
    args = {'user': request.user}
    return render(request, 'accounts/view_account_info.html')