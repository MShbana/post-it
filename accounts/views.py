from django.shortcuts import render


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/view_profile.html', args)